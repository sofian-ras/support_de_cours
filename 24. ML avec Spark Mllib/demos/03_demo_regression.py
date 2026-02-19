from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from itertools import chain
from pyspark.ml.feature import Imputer, StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler, MinMaxScaler, Bucketizer, SQLTransformer
from pyspark.sql.functions import sum as spark_sum
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.regression import LinearRegression, RandomForestRegressor, GBTRegressor
from pyspark.ml.evaluation import RegressionEvaluator
import time

spark = SparkSession.builder\
        .appName("demo_regression")\
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

preprocessing = Pipeline(stages=[
    imputer,
    total_rooms,
    multi_idx,
    ohe,
    bucketizer,
    assembler,
    std_scaler
])

# Fit uniquement sur TRAIN
pipeline_model = preprocessing.fit(train_df)

# Transform sur TRAIN et TEST
train_prepared = pipeline_model.transform(train_df)
test_prepared = pipeline_model.transform(test_df)

evaluator = RegressionEvaluator(labelCol="price", predictionCol="prediction")
results = {}

# Régression linéaire
lr = LinearRegression(
    featuresCol="features_std",
    labelCol="price",
    maxIter=100
)

pipeline_lr = Pipeline(stages=preprocessing.getStages() + [lr])
t0 = time.time()
model_lr = pipeline_lr.fit(train_df)
time_lr = time.time() - t0

pred_lr = model_lr.transform(test_df)

rmse_lr = evaluator.evaluate(pred_lr, {evaluator.metricName: "rmse"})
r2_lr = evaluator.evaluate(pred_lr, {evaluator.metricName: "r2"})
mae_lr = evaluator.evaluate(pred_lr, {evaluator.metricName: "mae"})
results["LinearRegression"] = {"RMSE" : rmse_lr, "R²": r2_lr, "MAE": mae_lr, "temps": time_lr}

print(f"RMSE : {rmse_lr} € | R² : {r2_lr} | MAE : {mae_lr} € | time : {time_lr}s")

# RandomForestRegressor

rf = RandomForestRegressor(
    featuresCol="features_std",
    labelCol="price",
    numTrees=50,
    seed=42
)

pipeline_rf = Pipeline(stages=preprocessing.getStages() + [rf])
t0 = time.time()
model_rf = pipeline_rf.fit(train_df)
time_rf = time.time() - t0

pred_rf = model_rf.transform(test_df)

rmse_rf = evaluator.evaluate(pred_rf, {evaluator.metricName: "rmse"})
r2_rf = evaluator.evaluate(pred_rf, {evaluator.metricName: "r2"})
mae_rf = evaluator.evaluate(pred_rf, {evaluator.metricName: "mae"})
results["RandomForest"] = {"RMSE" : rmse_rf, "R²": r2_rf, "MAE": mae_rf, "temps": time_rf}

print(f"RMSE : {rmse_rf} € | R² : {r2_rf} | MAE : {mae_rf} € | time : {time_rf}s")

# Feature importances
rf_model = model_rf.stages[-1]
importances = rf_model.featureImportances.toArray()
features_names = ["bedrooms_imp", "bathrooms_imp", "sqft_imp", "total_rooms", "age_years", "garage", "neighborhood_idx", "house_type_ohe"]
fi_pairs = sorted(zip(features_names[:len(importances)], importances), key=lambda x: -x[1])
# -x[1] : tri décroissant
for fname, importance in fi_pairs:
    bar = "|" * int(importance * 100)
    print(f"{fname} {importance} {bar}")

# GBT

gbt = GBTRegressor(
    featuresCol="features_std",
    labelCol="price",
    seed=42
)

pipeline_gbt = Pipeline(stages=preprocessing.getStages() + [gbt])
t0 = time.time()
model_gbt = pipeline_gbt.fit(train_df)
time_gbt = time.time() - t0

pred_gbt = model_gbt.transform(test_df)

rmse_gbt = evaluator.evaluate(pred_gbt, {evaluator.metricName: "rmse"})
r2_gbt = evaluator.evaluate(pred_gbt, {evaluator.metricName: "r2"})
mae_gbt = evaluator.evaluate(pred_gbt, {evaluator.metricName: "mae"})
results["GBT"] = {"RMSE" : rmse_gbt, "R²": r2_gbt, "MAE": mae_gbt, "temps": time_gbt}

print(f"RMSE : {rmse_gbt} € | R² : {r2_gbt} | MAE : {mae_gbt} € | time : {time_gbt}s")

for name, m in results.items():
    print(f"{name} : RMSE : {m['RMSE']} € | R² : {m['R²']} | MAE : {m['MAE']} € | time : {m['temps']}s")

spark.stop()