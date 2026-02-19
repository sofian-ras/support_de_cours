import time
import subprocess
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, rand, lit, expr,
    sum as spark_sum, isnan,
    min as f_min, max as f_max, avg,
    percentile_approx, corr, count
)
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import (
    Imputer, SQLTransformer,
    StringIndexer, OneHotEncoder,
    VectorAssembler, StandardScaler,
    MinMaxScaler, Bucketizer
)


spark = SparkSession.builder \
    .appName("TP_SoundStream_J1") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "1g") \
    .config("spark.sql.shuffle.partitions", "8") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

df = spark.read.option("header","true").option("inferSchema","true").csv("/data/streams.csv")

df.printSchema()
df.show(10)
print(f"{df.count()} lignes x {len(df.columns)} colonnes")

print("Nulls par colonne :")
null_df = df.select([
    spark_sum(when(col(c).isNull(), 1).otherwise(0)).alias(c)
    for c in df.columns
])
null_df.show()

n_rows = df.count()
print("Taux de nulls (%) :")
null_df.select([(col(c) / n_rows * 100).alias(c) for c in null_df.columns]).show()

print("Statistiques descriptives :")
df.describe().show()

print("Écoutes par genre :")
df.groupBy("genre").count().orderBy(col("count").desc()).show()

print("Écoutes par sub_type :")
df.groupBy("sub_type").count().orderBy(col("count").desc()).show()

print("Écoutes par device_type :")
df.groupBy("device_type").count().orderBy(col("count").desc()).show()

print("Distribution de engagement_score :")
df.select(
    f_min("engagement_score").alias("min"),
    f_max("engagement_score").alias("max"),
    avg("engagement_score").alias("moyenne"),
    percentile_approx("engagement_score", 0.25).alias("Q1"),
    percentile_approx("engagement_score", 0.5).alias("mediane"),
    percentile_approx("engagement_score", 0.75).alias("Q3"),
).show()

print("Distribution par tranche :")
df.select(
    when(col("engagement_score") < 25,  "[0-25[")
    .when(col("engagement_score") < 50,  "[25-50[")
    .when(col("engagement_score") < 75,  "[50-75[")
    .otherwise("[75-100]").alias("tranche")
).groupBy("tranche").count().orderBy("tranche").show()

print("Transformers")

imputer  = Imputer(
    inputCols=["listen_duration_s", "nb_likes"],
    outputCols=["listen_duration_imp", "nb_likes_imp"],
    strategy="median"
)
sql_tf = SQLTransformer(statement="""
    SELECT *,
        listen_duration_imp / 60.0                   AS listen_minutes,
        engagement_score / (nb_likes_imp + 1.0)      AS engagement_per_like,
        CASE WHEN hour_of_day BETWEEN 18 AND 22 THEN 1 ELSE 0 END AS peak_hour
    FROM __THIS__
""")
bucketizer = Bucketizer(splits=[0.0, 6.0, 12.0, 18.0, 24.0],
                           inputCol="hour_of_day", outputCol="time_slot")
str_indexer = StringIndexer(
    inputCols=["genre", "sub_type", "device_type"],
    outputCols=["genre_idx", "sub_type_idx", "device_type_idx"],
    handleInvalid="keep"
)
ohe = OneHotEncoder(
    inputCols=["genre_idx", "device_type_idx"],
    outputCols=["genre_ohe", "device_type_ohe"],
    dropLast=True
)
assembler = VectorAssembler(
    inputCols=[
        "listen_minutes", "nb_skips", "nb_likes_imp", "explicit_content",
        "peak_hour", "hour_of_day", "engagement_per_like",
        "time_slot",
        "sub_type_idx", "genre_ohe", "device_type_ohe"
    ],
    outputCol="features",
    handleInvalid="skip"
)
scaler = StandardScaler(inputCol="features", outputCol="features_scaled")

pipeline = Pipeline(stages=[
    imputer,
    sql_tf,
    bucketizer,
    str_indexer,
    ohe,
    assembler,
    scaler,
])

train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

pipeline_model = pipeline.fit(train_df)
train_prep = pipeline_model.transform(train_df)
test_prep  = pipeline_model.transform(test_df)

# Sauvegarde
pipeline_model.write().overwrite().save("/data/models/soundstream_pipeline")

# Rechargement
pipeline_reloaded = PipelineModel.load("/data/models/soundstream_pipeline")
test_reloaded     = pipeline_reloaded.transform(test_df)

spark.stop()
