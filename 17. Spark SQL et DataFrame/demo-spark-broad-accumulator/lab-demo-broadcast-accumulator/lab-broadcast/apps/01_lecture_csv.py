from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg, count, col



spark = SparkSession.builder \
    .appName("demo") \
    .master("spark://spark-master:7077") \
    .config("spark.ui.showConsoleProgress", "false") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")


transactions = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("/data/transactions.csv")

transactions.printSchema()

transactions.show(10)


transactions.groupBy("ville") \
    .agg(
        count("*").alias("nb_transactions"),
        sum("montant").alias("ca_total"),
        avg("montant").alias("panier_moyen")
    ) \
    .orderBy(col("ca_total").desc()) \
    .show()