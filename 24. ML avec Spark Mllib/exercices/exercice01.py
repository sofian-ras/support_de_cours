import os
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, sum as spark_sum, when, rand, lit,
    min as spark_min, max as spark_max, avg,
    percentile_approx, create_map, median
)
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import (
    StringIndexer, OneHotEncoder, Imputer,
    VectorAssembler, StandardScaler, SQLTransformer, Bucketizer
)

spark = SparkSession.builder \
    .appName("Exercice_Jour1_Fitness") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "1g") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print("Chargement et exploration")

df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("/data/fitness_sessions.csv")

print("Schema :")
df.printSchema()

df.show(5)

n_rows = df.count()
n_cols = len(df.columns)
print(f"Dimensions : {n_rows} lignes x {n_cols} colonnes")

print("Statistiques descriptives :")
df.describe().show()

print("Valeurs nulles par colonne :")
df.select([
    spark_sum(when(col(c).isNull(), 1).otherwise(0)).alias(c)
    for c in df.columns
]).show()

print("Statistiques sur 'calories_burned' :")
df.select(
    spark_min("calories_burned").alias("min"),
    spark_max("calories_burned").alias("max"),
    avg("calories_burned").alias("moyenne"),
    median("calories_burned").alias("mediane")
).show()

print("Calories moyennes par type d'activite :")
df.groupBy("activity_type") \
  .agg(avg("calories_burned").alias("avg_calories")) \
  .orderBy("avg_calories", ascending=False) \
  .show()


print("Preparation des donnees")

imputer = Imputer(
    inputCols=["duration_minutes", "heart_rate_avg", "steps_count"],
    outputCols=["duration_imp", "heart_rate_imp", "steps_imp"],
    strategy="median"
)

# effort_score + is_active_sport
sql_transformer = SQLTransformer(
    statement="""
        SELECT *,
            (heart_rate_imp * duration_imp / 60.0) AS effort_score,
            CASE WHEN activity_type IN ('running', 'cycling', 'swimming')
                 THEN 1 ELSE 0 END AS is_active_sport
        FROM __THIS__
    """
)

# StringIndexer pour activity_type
activity_indexer = StringIndexer(
    inputCol="activity_type",
    outputCol="activity_idx",
    handleInvalid="keep"
)

# StringIndexer + OneHotEncoder pour intensity_level
intensity_indexer = StringIndexer(
    inputCol="intensity_level",
    outputCol="intensity_idx",
    handleInvalid="keep"
)
intensity_ohe = OneHotEncoder(
    inputCols=["intensity_idx"],
    outputCols=["intensity_ohe"],
    dropLast=True
)

# VectorAssembler
assembler = VectorAssembler(
    inputCols=[
        "duration_imp", "heart_rate_imp", "steps_imp",
        "distance_km", "sleep_hours_prev", "user_age", "is_morning",
        "effort_score", "is_active_sport",
        "activity_idx", "intensity_ohe"
    ],
    outputCol="features",
    handleInvalid="skip"
)

# StandardScaler
scaler = StandardScaler(
    inputCol="features",
    outputCol="features_scaled",
    withMean=True,
    withStd=True
)

print("Pipeline complet")

pipeline = Pipeline(stages=[
    imputer,
    sql_transformer,
    activity_indexer,
    intensity_indexer,
    intensity_ohe,
    assembler,
    scaler,
])

train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

pipeline_model = pipeline.fit(train_df)
test_prepared  = pipeline_model.transform(test_df)
train_prepared = pipeline_model.transform(train_df)

models_path = "/data/models/fitness_pipeline"

# Sauvegarde
pipeline_model.write().overwrite().save(models_path)

# Rechargement
pipeline_loaded = PipelineModel.load(models_path)
test_reloaded   = pipeline_loaded.transform(test_df)

test_prepared.select("features_scaled").show(3, truncate=False)
test_reloaded.select("features_scaled").show(3, truncate=False)