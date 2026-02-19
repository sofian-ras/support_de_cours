from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, DoubleType
from pyspark.sql.functions import udf, col

# Créer la session Spark
spark = SparkSession.builder.master("local").appName("demo-udf").getOrCreate()

data = [
    ("Toto", 25, "Ingénieur", 50000.0),
    ("Tata", 38, "Manager", 60000.0),
    ("Titi", 35, "Dév", 30000.0)
]

df = spark.createDataFrame(data, ["nom", "age", "poste", "salaire"])

# Définir l'udf
def categorie_age(age):
    if age < 30:
        return "Junior"
    elif age < 40 :
        return "Expérimenté"
    else: 
        return "Senior"
    
def salaire_avec_bonus(salaire):
    return salaire * 1.10

categorieAge = udf(categorie_age, StringType())
salaireBonus = udf(salaire_avec_bonus, DoubleType())

dfWithUdf = df.withColumn("categorie_age", categorieAge(col("age"))) \
                .withColumn("salaire_avec_bonus", salaireBonus(col("salaire")))

dfWithUdf.show()