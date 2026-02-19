from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructField, StructType, StringType, IntegerType
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("demo_window") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

data = [
    ("Alice", "Nord", "2024-01", 1500),
    ("Alice", "Nord", "2024-02", 2000),
    ("Alice", "Nord", "2024-03", 1800),
    ("Bob", "Nord", "2024-01", 1200),
    ("Bob", "Nord", "2024-02", 1600),
    ("Bob", "Nord", "2024-03", 1400),
    ("Charlie", "Sud", "2024-01", 2200),
    ("Charlie", "Sud", "2024-02", 2500),
    ("Charlie", "Sud", "2024-03", 2300),
    ("Diana", "Sud", "2024-01", 1800),
    ("Diana", "Sud", "2024-02", 2100),
    ("Diana", "Sud", "2024-03", 1900),
    ("Eve", "Est", "2024-01", 1700),
    ("Eve", "Est", "2024-02", 1900),
    ("Eve", "Est", "2024-03", 2200),
]

schema = StructType([
    StructField("vendeur", StringType(), True),
    StructField("region", StringType(), True),
    StructField("mois", StringType(), True),
    StructField("ventes", IntegerType(), True)
])

df = spark.createDataFrame(data, schema)

# dfGroupBy = df.groupBy("region").agg(F.avg("ventes").alias("ventes_moyennes"))

# dfGroupBy.show()

# window_region = Window.partitionBy("region")

# df = df.withColumn(
#     "ventes_moyennes_dept",
#     F.avg("ventes").over(window_region)
# )

# df.show()

# # Fonctions de ranking
# window_rank_region = Window.partitionBy("region").orderBy(F.col("ventes").desc())

# # row_number => numéro séquentiel unique (1,2,3,4...)
# # rank => même rang pour ex-aequo puis saute (1, 2, 2, 4, 5)
# # dense_rank => même rang pour ex-aequo sans saute (1, 2, 2, 3, 4)
# df = df.withColumn("row_number", F.row_number().over(window_rank_region))\
#         .withColumn("rank", F.rank().over(window_rank_region))\
#         .withColumn("dense_rank", F.dense_rank().over(window_rank_region))

# df.show()

# # Fonction LAG & LEAD (accès aux lignes adjacentes)
# window_vendeur = Window.partitionBy("vendeur").orderBy("mois")

# df = df.withColumn("ventes_mois_precedent", F.lag("ventes", 1).over(window_vendeur))\
#         .withColumn("ventes_mois_suivant", F.lead("ventes", 1).over(window_vendeur))\
#         .withColumn("variation_precedent", F.col("ventes") - F.lag("ventes", 1).over(window_vendeur))

# df.show()

# # sur plusieurs mois
# window_frame = Window.partitionBy("vendeur").orderBy("mois").rowsBetween(-2, 0) # 2 lignes avant jusqu'à ligne courante

# df = df.withColumn(
#     "moyenne_sur_3mois",
#     F.avg("ventes").over(window_frame)
# )

# Trouver les 2 meilleurs vendeurs par région
window_top = Window.partitionBy("region").orderBy(F.col("ventes").desc())

df = df.withColumn("rang", F.row_number().over(window_top))\
        .filter(F.col("rang") <= 2).orderBy("region", "rang")

df.show()

