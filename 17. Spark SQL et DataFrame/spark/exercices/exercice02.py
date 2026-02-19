from pyspark.sql import SparkSession
from pyspark.sql.functions import col, min, max, avg
# from pyspark.sql import functions as F

# Créer la session Spark
spark = SparkSession.builder.master("local").appName("exercice-02").getOrCreate()

df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .option("sep", ",") \
        .csv("./data/housing.csv")

# 1. Calculer min, max, moyenne pour median_house_value
df.select(
    min("median_house_value").alias("min_value"),
    max("median_house_value").alias("max_value"),
    avg("median_house_value").alias("avg_value"),
).show()

# 2. Calculer min, max, moyenne pour median_income
df.select(
    min("median_income").alias("min_value"),
    max("median_income").alias("max_value"),
    avg("median_income").alias("avg_value"),
).show()

# 3. Calculer min, max, moyenne pour housing_median_age
df.select(
    min("housing_median_age").alias("min_value"),
    max("housing_median_age").alias("max_value"),
    avg("housing_median_age").alias("avg_value"),
).show()


# 4. Compter combien de districts ont une population > 5000
count = df.filter(col("population") > 5000).count()

print(f"Le nombre de districts avec population > 5000 : {count}")

# 5. Prix moyen des maisons par type de proximité océan
# 6. Revenu moyen par type de proximité océan
# 7. Âge moyen des maisons par type de proximité océan
# 8. Population moyenne par type de proximité océan
df.groupBy("ocean_proximity") \
    .agg(
        avg("median_house_value").alias("prix_moyen"),
        avg("median_income").alias("revenu_moyen"),
        avg("housing_median_age").alias("age_moyen"),
        avg("population").alias("population_moyen"),
    ).orderBy(col("prix_moyen").desc()).show()