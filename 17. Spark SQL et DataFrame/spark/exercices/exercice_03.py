from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Créer la session Spark
spark = SparkSession.builder.master("local").appName("demo-join").getOrCreate()

movieDf = spark.read \
         .option("header", "true") \
         .option("inferSchema", "true") \
         .option("sep", ",") \
         .csv("./data/movie.csv")   

ratingDf = spark.read \
         .option("header", "true") \
         .option("inferSchema", "true") \
         .option("sep", ",") \
         .csv("./data/rating.csv")   

# print(movieDf.count())
# print(ratingDf.count())

# Faire un **inner join** entre `ratings` et `movies` sur `movieId`
# df = ratingDf.join(movieDf, ["movieId"], "inner")
# df.show()

# # - Calculer le nombre de notes et la moyenne des notes par film
# # - Trier par nombre de notes décroissant
# ratingDf.groupBy("movieId").agg(
#     F.count("rating").alias("nb_rating"),
#     F.avg("rating").alias("avg_rating")
# ).join(movieDf, ["movieId"], "inner").orderBy(F.desc("nb_rating")).show()

# # - **LEFT SEMI** : films qui ont au moins une note
# ratingDf.join(movieDf, ["movieId"], "left_semi")
# # - **LEFT ANTI** : films sans aucune note
# movieDf.join(ratingDf, ["movieId"], "left_anti")
# # - **LEFT OUTER** : liste complète des films avec stats si disponibles
# movieDf.join(ratingDf, ["movieId"], "left_outer").groupBy("rating").agg(
#     F.count("rating").alias("nb_rating"),
#     F.avg("rating").alias("avg_rating")
# ).orderBy("rating").show()
# # - **FULL OUTER** : diagnostic des clés présentes uniquement dans l’un des deux fichiers
# movieDf.join(ratingDf, ["movieId"], "full")

# **Top 5 global** : films les mieux notés
ratingDf.groupBy("movieId").agg(
    F.count("rating").alias("nb_rating"),
    F.avg("rating").alias("avg_rating")
).filter(F.col("nb_rating") >= 50).join(movieDf,["movieId"], "inner").orderBy(F.desc("avg_rating")).show(5)