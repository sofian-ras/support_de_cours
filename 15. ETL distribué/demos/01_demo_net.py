from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, trim, coalesce

spark = SparkSession.builder \
    .appName("TP_Broadcast_Accumulator_Correction") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

df = spark.read.csv("/data/ventes.csv", header=True, inferSchema=True)

df.show()

df.select([
    count(when(col(c).isNull(), c)).alias(c +"_nulls")
    for c in df.columns
]).show()

# Problème 1 : Valeur nulle dans la colonne 'produit'
df.filter(col('produit').isNull()).show()

# Solution : supprimer les lignes 
df_cleaned = df.filter(col("produit").isNotNull())

df_cleaned.show()

# Problème 2 : valeurs négatives dans 'quantite'
df_cleaned.filter(col('quantite') < 0).show()

# Solution : Remplacer pas la valeur absolue
from pyspark.sql.functions import abs as abs_spark
df_cleaned = df_cleaned.withColumn(
    "quantite",
    when(col("quantite") < 0, abs_spark(col("quantite"))).otherwise(col("quantite"))
)

df_cleaned.show()

# Problème 3 : Quantitée à 0
df_cleaned.filter(col('quantite') == 0).show()

# Solution : Supprimer ces lignes
df_cleaned = df_cleaned.filter(col("quantite") > 0)

df_cleaned.show()

# Problème 4 : Valeurs nulles dans 'client'
df_cleaned.filter(col('client').isNull()).show()

# Solution : Remplacer pas 'client anonyme'
df_cleaned = df_cleaned.withColumn(
    "client",
    when(
        (col("client").isNull()) |
        (col("client") == "NULL") |
        (trim(col("client")) == ""),
        "Client anonyme"
    ).otherwise(col("client"))
)

df_cleaned.show()

# problème 5 : date manquante
df_cleaned.filter(col('date').isNull()).show()

# Solution : Supprimer la ligne
df_cleaned = df_cleaned.filter(col('date').isNotNull())

df_cleaned.show()

# Problème 6 : prix unitaire manquant
df_cleaned.filter(col('prix_unitaire').isNull()).show()

# Solution : Calculer le prix moyen
prix_moyen = df_cleaned.groupBy("produit").agg({"prix_unitaire" : "avg"}).withColumnRenamed("avg(prix_unitaire)", "prix_moyen")

df_cleaned = df_cleaned.join(prix_moyen, ["produit"], "left")
df_cleaned = df_cleaned.withColumn(
    "prix_unitaire",
    coalesce(col("prix_unitaire"), col("prix_moyen"))
).drop("prix_moyen")

df_cleaned.show()

# Sauvegarde du csv propre
df_cleaned.repartition(3).write.mode("overwrite").option("header", "true").csv("/data/output/ventes_clean")

spark.stop()