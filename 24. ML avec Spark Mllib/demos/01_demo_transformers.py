from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from itertools import chain
from pyspark.ml.feature import Imputer, StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler, MinMaxScaler, Bucketizer, SQLTransformer
from pyspark.sql.functions import sum as spark_sum

spark = SparkSession.builder\
        .appName("demo_transformers")\
        .master("spark://spark-master:7077")\
        .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

neighborhood_map = {0: "Centre", 1: "Nord", 2: "Sud", 3: "Est", 4: "Ouest"}
house_type_map   = {0: "house", 1: "apartment", 2: "studio"}
n_map = create_map([lit(x) for x in chain(*neighborhood_map.items())])
h_map = create_map([lit(x) for x in chain(*house_type_map.items())])

df = spark.range(100).select(
    n_map[(rand(seed=1) * 5).cast("int").cast("string")].alias("neighborhood"),
    h_map[(rand(seed=2) * 3).cast("int").cast("string")].alias("house_type"),
    when(rand(seed=3) > 0.15, (rand(seed=3) * 4 + 1).cast("int")).otherwise(None).alias("bedrooms"),
    when(rand(seed=4) > 0.10, (rand(seed=4) * 3 + 1).cast("int")).otherwise(None).alias("bathrooms"),
    when(rand(seed=5) > 0.12, (rand(seed=5) * 150 + 30).cast("float")).otherwise(None).alias("sqft"),
    (rand(seed=6) * 50).cast("int").alias("age_years"),
    (rand(seed=7) > 0.4).cast("int").alias("garage"),
    (rand(seed=8) * 300000 + 80000).cast("float").alias("price"),
)

df.show(6)

df.select([
    spark_sum(when(col(c).isNull(), 1).otherwise(0)).alias(c)
    for c in df.columns
]).show()

# Imputer - Remplacement des valeurs manquantes
imputer = Imputer(
    inputCols=["bedrooms", "bathrooms", "sqft"],
    outputCols=["bedrooms_imp", "bathrooms_imp", "sqft_imp"],
    strategy="median"
)

imputer_model = imputer.fit(df)
df_imputed = imputer_model.transform(df)

df_imputed.select([
    spark_sum(when(col(c).isNull(), 1).otherwise(0)).alias(c)
    for c in df_imputed.columns
]).show()

# SQLTransformer : ajout de nouvelles features
# __THIS__ désigne le df en entrée
total_rooms = SQLTransformer(
    statement="SELECT *, (bedrooms_imp + bathrooms_imp) AS total_rooms FROM __THIS__"
)

df_tr = total_rooms.transform(df_imputed)

# StringIndexer - Encodage catégoriel => numérique

"""
handleInvalid :
    - skip => supprime la ligne
    - error => Lève une erreur
    - keep => assigne un index spécial (nb_categories)
"""
multi_idx = StringIndexer(
    inputCols=["neighborhood", "house_type"],
    outputCols=["neighborhood_idx", "house_type_idx"],
    handleInvalid="keep"
)

model_multi = multi_idx.fit(df_tr)
df_idx = model_multi.transform(df_tr)

# OneHotEncoder : index => vecteur binaire

ohe = OneHotEncoder(
    inputCol='house_type_idx',
    outputCol='house_type_ohe',
    dropLast=True
)

ohe_model = ohe.fit(df_idx)
df_ohe = ohe_model.transform(df_idx)

df_ohe.select("house_type", "house_type_idx", "house_type_ohe").show()

# Bucketizer - transforme une variable continue en tranche
"""
exemple : [0, 10, 30, 200]
    bucket 0 : [0,10[
    bucket 1 : [10, 30[
    bucket 2 : [30, 200[
"""
bucketizer = Bucketizer(
    splits=[0, 10, 30, 200],
    inputCol="age_years",
    outputCol="age_bucket"
)

df_bucket = bucketizer.transform(df_ohe)

df_bucket.select("age_years", "age_bucket").show(10)

# VectorAssembler - assemblage en vecteur features
assembler = VectorAssembler(
    inputCols=["bedrooms_imp", "bathrooms_imp", "sqft_imp",
               "total_rooms", "age_bucket", "neighborhood_idx",
               "house_type_ohe", "garage"], # equivalent de X
    outputCol="features",
    handleInvalid="skip"
)

df_assembled = assembler.transform(df_bucket)

df_assembled.select("features").show(truncate=False)

# StandardScaler - Standardisation

std_scaler = StandardScaler(
    inputCol="features",
    outputCol="features_std"
)

std_model = std_scaler.fit(df_assembled)
df_std = std_model.transform(df_assembled)

df_std.select("features_std").show(truncate=False)

spark.stop()