from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from itertools import chain
from pyspark.ml.feature import Imputer, StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler, MinMaxScaler, Bucketizer, SQLTransformer
from pyspark.sql.functions import sum as spark_sum
from pyspark.ml import Pipeline, PipelineModel

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


# SQLTransformer : ajout de nouvelles features
# __THIS__ désigne le df en entrée
total_rooms = SQLTransformer(
    statement="SELECT *, (bedrooms_imp + bathrooms_imp) AS total_rooms FROM __THIS__"
)


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

# OneHotEncoder : index => vecteur binaire
ohe = OneHotEncoder(
    inputCol='house_type_idx',
    outputCol='house_type_ohe',
    dropLast=True
)


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

# VectorAssembler - assemblage en vecteur features
assembler = VectorAssembler(
    inputCols=["bedrooms_imp", "bathrooms_imp", "sqft_imp",
               "total_rooms", "age_bucket", "neighborhood_idx",
               "house_type_ohe", "garage"], # equivalent de X
    outputCol="features",
    handleInvalid="skip"
)

# StandardScaler - Standardisation
std_scaler = StandardScaler(
    inputCol="features",
    outputCol="features_std"
)

train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

pipeline = Pipeline(stages=[
    imputer,
    total_rooms,
    multi_idx,
    ohe,
    bucketizer,
    assembler,
    std_scaler
])

# Fit uniquement sur TRAIN
pipeline_model = pipeline.fit(train_df)

# Transform sur TRAIN et TEST
train_prepared = pipeline_model.transform(train_df)
test_prepared = pipeline_model.transform(test_df)

# Sauvegarde et chargement de la pipeline
save_path = "/data/models/demo_house_pipeline"

# Sauvegarde
pipeline_model.write().overwrite().save(save_path)

# Chargement
pipeline_reload = PipelineModel.load(save_path)

test_reload = pipeline_reload.transform(test_df)

spark.stop()