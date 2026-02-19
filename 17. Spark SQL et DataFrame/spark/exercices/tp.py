
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, DoubleType

spark = SparkSession.builder.master("local").appName("TP").getOrCreate()

# ### Partie 1 : Chargement et exploration



# 1. Charger le CSV en DataFrame avec l'option header
df = spark.read\
            .option("header", "true") \
            .option("inferSchema", "true") \
            .option("quote", "\"") \
            .option("escape", "\"") \
            .option("multiline", "true") \
            .csv("./data/Sample_Superstore.csv")

# 2. Afficher le schéma du DataFrame
df.printSchema()

# 3. Afficher les 20 premières lignes
df.show(20)
# 4. Compter le nombre total de lignes
print(df.count())

# 5. Afficher les régions uniques (colonne `Region`)
df.select("Region").distinct().show()

# ### Partie 2 : Transformations simples

# 1. Créer une colonne `Profit Margin` = `Profit` / `Sales`
dfWithMargin = df.withColumn(
    "Profit Margin",
    F.col("Profit").cast("double") / F.col("Sales").cast("double")
)

# 2. Créer une colonne `Year` en extrayant l'année de `Order Date`
dfWithYear = dfWithMargin.withColumn(
    "Year",
    F.year(F.to_timestamp(F.col("Order Date"), "M/d/yyyy"))
)

# 3. Créer une colonne `Total Value` = `Sales` - `Discount`
dfFinal = dfWithYear.withColumn(
    "Total Value",
    F.col("Sales").cast("double") - F.col("Discount").cast("double")
)

# 4. Afficher les 10 premières lignes avec ces nouvelles colonnes
dfFinal.show()
# 5. **Mettre ce DataFrame en cache** (vous allez le réutiliser plusieurs fois)
dfFinal.cache()

# ### Partie 3 : UDF - Catégorisation des ventes

# 1. Créer une UDF `categorizeSale` qui prend le montant `Sales` et retourne :

#    - "Petite vente" si < 100$
#    - "Vente moyenne" si entre 100$ et 500$
#    - "Grosse vente" si > 500$

def catecorize_sale_func(sales):
    if sales < 100:
        return "Petite vente"
    elif 100 <= sales <= 500:
        return "Vente moyenne"
    else:
        return "Grosse vente"
    
categorizeSale = F.udf(catecorize_sale_func, StringType())

# 2. Appliquer cette UDF pour créer une colonne `Sale Category`
dfWithCategory = dfFinal.withColumn("Sale Category", categorizeSale(F.col("Sales")))
# 3. Afficher quelques lignes avec cette nouvelle colonne
dfWithCategory.show()
# 4. Compter le nombre de ventes par catégorie (Petite/Moyenne/Grosse)
dfWithCategory.groupBy("Sale Category").count().orderBy(F.desc("count")).show()

# ### Partie 4 : UDF - Niveau de remise

# 1. Créer une UDF `discountLevel` qui prend `Discount` et retourne :

#    - "Pas de remise" si = 0
#    - "Remise faible" si entre 0 et 0.2
#    - "Remise forte" si > 0.2

def discount_level_func(discount):
    if discount == 0:
        return "Pas de remise"
    elif 0 <= discount <= 0.2:
        return "Remise faible"
    else:
        return "Remise forte"
    
discountLevel = F.udf(discount_level_func, StringType())

# 2. Appliquer cette UDF pour créer une colonne `Discount Level`
dfWithDiscount = dfWithCategory.withColumn("Discount Level", categorizeSale(F.col("Discount")))

dfWithDiscount.show()

# 3. Calculer le CA total par niveau de remise
dfWithDiscount.groupBy("Discount Level").agg(
    sum("Sales").alias("CA Total"),
    F.count("*").alias("Nombre de ventes")
).show()

# ### Partie 5 : Agrégations basiques

# 1. Calculer le CA total (`Sales`) par région
dfWithDiscount.groupBy("Region") \
    .agg(sum("Profit").alias("Profit Total")).show()

# 2. Calculer le profit total par catégorie de produit (`Category`)
dfWithDiscount.groupBy("Category") \
    .agg(sum("Profit").alias("Profit Total")).show()
# 3. Calculer le nombre de commandes par segment client (`Segment`)
dfWithDiscount.groupBy("Segment") \
    .agg(F.countDistinct("Order ID").alias("Nombre de commandes")).show()
# 4. Identifier les 10 produits (`Product Name`) les plus vendus en quantité
dfWithDiscount.groupBy("Product Name") \
    .agg(sum("Quantity").alias("Quantité Total")).show()
# 5. Identifier les 5 états (`State`) avec le plus de CA
dfWithDiscount.groupBy("State") \
    .agg(sum("Sales").alias("CA Total")).show()

# ### Partie 6 : Broadcast Variable - Codes région

# 1. Créer une Map qui associe chaque région à un code :

# ```scala
# val regionCodes = Map(
#   "East" -> "EST",
#   "West" -> "WST",
#   "Central" -> "CTR",
#   "South" -> "STH"
# )
# ```
regionCode = {
    "East" : "EST",
    "West" : "WST",
    "Central" : "CTR",
    "South" : "STH"
}

# 2. Broadcaster cette Map avec `spark.sparkContext.broadcast()`
broadcastRegionCodes = spark.sparkContext.broadcast(regionCode)

# 3. Créer une UDF qui utilise cette broadcast variable pour créer une colonne `Region Code`
def get_region_code_func(region):
    return broadcastRegionCodes.value.get(region, "UNKNOWN")

getRegionCode = F.udf(get_region_code_func, StringType())

dfWithRegion = dfWithDiscount.withColumn("Region Code", getRegionCode(F.col("Region")))
# 4. Afficher quelques lignes avec le code région
dfWithRegion.show()

# ### Partie 7 : Broadcast Variable - Coefficients de priorité

# 1. Créer une Map de coefficients par catégorie :

# ```scala
# val categoryPriority = Map(
#   "Technology" -> 1.5,
#   "Furniture" -> 1.2,
#   "Office Supplies" -> 1.0
# )
# ```

# 2. Broadcaster cette Map

# 3. Créer une UDF qui multiplie le `Profit` par le coefficient de sa catégorie pour créer une colonne `Weighted Profit`

# 4. Calculer le weighted profit total par catégorie

categoryPriority = {
  "Technology" : 1.5,
  "Furniture" : 1.2,
  "Office Supplies" : 1.0
}

broadcastCategoryPriority = spark.sparkContext.broadcast(categoryPriority)

def get_weighted_profit_func(profit, category):
    coef = broadcastCategoryPriority.value.get(category, 1.0)
    return profit * coef

getWeightedProfit = F.udf(get_weighted_profit_func, DoubleType())

dfFinal = dfWithDiscount.withColumn("Weighted Profit", getWeightedProfit(F.col("Profit"), F.col("Category")))

dfFinal.show()

dfFinal.groupBy("Category")\
.agg(
    sum("Profit").alias("Profit total"),
    sum("Weighted Profit").alias("Profit total weighted"),
).show()


dfFinal.unpersist()