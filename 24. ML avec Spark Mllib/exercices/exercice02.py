import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, avg
)
from pyspark.ml import Pipeline
from pyspark.ml.feature import (
    Imputer, SQLTransformer, StringIndexer, OneHotEncoder,
    VectorAssembler, StandardScaler
)
from pyspark.ml.regression import (
    LinearRegression, RandomForestRegressor, GBTRegressor
)
from pyspark.ml.classification import (
    LogisticRegression, RandomForestClassifier, GBTClassifier
)
from pyspark.ml.evaluation import (
    RegressionEvaluator,
    MulticlassClassificationEvaluator
)

spark = SparkSession.builder \
    .appName("Correction_Meteo") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "1g") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print("PARTIE A")

df_weather = spark.read.csv("/data/weather_data.csv", header=True, inferSchema=True)
total_weather = df_weather.count()
print(f"{total_weather} lignes")
print("Schéma :")
df_weather.printSchema()
print("Statistiques de temperature_max :")
df_weather.select("temperature_max").describe().show()

# Analyse exploratoire
print("Température moyenne par saison (décroissant) :")
df_weather.groupBy("season") \
    .agg(avg("temperature_max").alias("temp_moy")) \
    .orderBy("temp_moy", ascending=False) \
    .show()

print("Température moyenne par région (décroissant) :")
df_weather.groupBy("region") \
    .agg(avg("temperature_max").alias("temp_moy")) \
    .orderBy("temp_moy", ascending=False) \
    .show()

nulls_humidity = df_weather.filter(col("humidity").isNull()).count()
nulls_pressure = df_weather.filter(col("pressure_hpa").isNull()).count()
print(f"Valeurs nulles — humidity : {nulls_humidity}  |  pressure_hpa : {nulls_pressure}")

train_weather, test_weather = df_weather.randomSplit([0.8, 0.2], seed=42)

# Pipeline de prétraitement
imputer_w = Imputer(
    inputCols=["humidity", "pressure_hpa"],
    outputCols=["humidity_imp", "pressure_imp"],
    strategy="median"
)
interaction_w = SQLTransformer(
    statement="SELECT *, (humidity_imp * uv_index / 10.0) AS temp_humidity_interaction FROM __THIS__"
)
season_idx_w = StringIndexer(inputCol="season", outputCol="season_idx", handleInvalid="keep")
region_idx_w = StringIndexer(inputCol="region", outputCol="region_idx", handleInvalid="keep")
season_ohe_w = OneHotEncoder(inputCols=["season_idx"], outputCols=["season_ohe"], dropLast=True)
region_ohe_w = OneHotEncoder(inputCols=["region_idx"], outputCols=["region_ohe"], dropLast=True)
assembler_w = VectorAssembler(
    inputCols=[
        "month", "humidity_imp", "pressure_imp", "wind_speed_kmh",
        "cloud_cover_pct", "uv_index", "temp_humidity_interaction",
        "season_ohe", "region_ohe"
    ],
    outputCol="features",
    handleInvalid="skip"
)
scaler_w = StandardScaler(inputCol="features", outputCol="features_scaled", withMean=True, withStd=True)

preprocessing_w = Pipeline(stages=[
    imputer_w, interaction_w, season_idx_w, region_idx_w,
    season_ohe_w, region_ohe_w, assembler_w, scaler_w
])

FEATURE_NAMES_W = [
    "month", "humidity_imp", "pressure_imp", "wind_speed_kmh",
    "cloud_cover_pct", "uv_index", "temp_humidity_interaction",
    "season_ohe", "region_ohe"
]

reg_evaluator = RegressionEvaluator(labelCol="temperature_max", predictionCol="prediction")
regression_results = {}

print("LinearRegression :")
lr = LinearRegression(
    featuresCol="features_scaled", labelCol="temperature_max",
    maxIter=100, regParam=0.1
)
pipeline_lr = Pipeline(stages=preprocessing_w.getStages() + [lr])
t0 = time.time()
model_lr = pipeline_lr.fit(train_weather)
elapsed_lr = time.time() - t0
preds_lr = model_lr.transform(test_weather)
rmse_lr = reg_evaluator.evaluate(preds_lr, {reg_evaluator.metricName: "rmse"})
r2_lr   = reg_evaluator.evaluate(preds_lr, {reg_evaluator.metricName: "r2"})
mae_lr  = reg_evaluator.evaluate(preds_lr, {reg_evaluator.metricName: "mae"})
regression_results["LinearRegression"] = {"RMSE": rmse_lr, "R2": r2_lr, "MAE": mae_lr, "temps": elapsed_lr}
print(f"  RMSE : {rmse_lr:.4f}  |  R² : {r2_lr:.4f}  |  MAE : {mae_lr:.4f}  |  Temps : {elapsed_lr:.2f}s")

print("RandomForestRegressor :")
rf = RandomForestRegressor(
    featuresCol="features_scaled", labelCol="temperature_max",
    numTrees=100, maxDepth=6, seed=42
)
pipeline_rf = Pipeline(stages=preprocessing_w.getStages() + [rf])
t0 = time.time()
model_rf = pipeline_rf.fit(train_weather)
elapsed_rf = time.time() - t0
preds_rf = model_rf.transform(test_weather)
rmse_rf = reg_evaluator.evaluate(preds_rf, {reg_evaluator.metricName: "rmse"})
r2_rf   = reg_evaluator.evaluate(preds_rf, {reg_evaluator.metricName: "r2"})
mae_rf  = reg_evaluator.evaluate(preds_rf, {reg_evaluator.metricName: "mae"})
regression_results["RandomForest"] = {"RMSE": rmse_rf, "R2": r2_rf, "MAE": mae_rf, "temps": elapsed_rf}
print(f"  RMSE : {rmse_rf:.4f}  |  R² : {r2_rf:.4f}  |  MAE : {mae_rf:.4f}  |  Temps : {elapsed_rf:.2f}s")

print("GBTRegressor :")
gbt = GBTRegressor(
    featuresCol="features_scaled", labelCol="temperature_max",
    maxIter=50, stepSize=0.1, maxDepth=4, seed=42
)
pipeline_gbt = Pipeline(stages=preprocessing_w.getStages() + [gbt])
t0 = time.time()
model_gbt = pipeline_gbt.fit(train_weather)
elapsed_gbt = time.time() - t0
preds_gbt = model_gbt.transform(test_weather)
rmse_gbt = reg_evaluator.evaluate(preds_gbt, {reg_evaluator.metricName: "rmse"})
r2_gbt   = reg_evaluator.evaluate(preds_gbt, {reg_evaluator.metricName: "r2"})
mae_gbt  = reg_evaluator.evaluate(preds_gbt, {reg_evaluator.metricName: "mae"})
regression_results["GBT"] = {"RMSE": rmse_gbt, "R2": r2_gbt, "MAE": mae_gbt, "temps": elapsed_gbt}
print(f"  RMSE : {rmse_gbt:.4f}  |  R² : {r2_gbt:.4f}  |  MAE : {mae_gbt:.4f}  |  Temps : {elapsed_gbt:.2f}s")


print("Tableau comparatif :")
for mname, metrics in regression_results.items():
    print(f"  {mname} {metrics['RMSE']} {metrics['R2']} "
          f"{metrics['MAE']} {metrics['temps']}")

# meilleur modèle
best_reg_name = min(regression_results, key=lambda x: regression_results[x]["RMSE"])
print(f"Meilleur modèle : {best_reg_name}")

if best_reg_name in ("RandomForest", "GBT"):
    best_reg_model = {"RandomForest": model_rf, "GBT": model_gbt}[best_reg_name]
    importances = best_reg_model.stages[-1].featureImportances.toArray()
    fi_pairs = sorted(zip(FEATURE_NAMES_W, importances), key=lambda x: -x[1])
    print(f"Top 5 features les plus importantes ({best_reg_name}) :")
    for fname, importance in fi_pairs[:5]:
        bar = "|" * int(importance * 100)
        print(f"  {fname:<35} {importance:.4f}  {bar}")


# ========= PARTIE B =========

df_rain = spark.read.csv("/data/rain_prediction.csv", header=True, inferSchema=True)
total_rain = df_rain.count()
print(f"{total_rain} lignes")
print("Distribution de will_rain :")
dist_rain = df_rain.groupBy("will_rain").count().orderBy("will_rain")
dist_rain.show()

count_rain = df_rain.filter(col("will_rain") == 1).count()
pct_rain = count_rain / total_rain * 100
print(f"Taux de pluie : {pct_rain:.1f}% — ", end="")
if 40 <= pct_rain <= 60:
    print("classes équilibrées")
else:
    print("classes déséquilibrées")

# Split train / test
train_rain, test_rain = df_rain.randomSplit([0.8, 0.2], seed=42)

imputer_r = Imputer(
    inputCols=["humidity", "pressure_hpa", "dew_point"],
    outputCols=["humidity_imp", "pressure_imp", "dew_point_imp"],
    strategy="median"
)
season_idx_r = StringIndexer(inputCol="season", outputCol="season_idx", handleInvalid="keep")
region_idx_r = StringIndexer(inputCol="region", outputCol="region_idx", handleInvalid="keep")
ohe_r = OneHotEncoder(
    inputCols=["season_idx", "region_idx"],
    outputCols=["season_ohe", "region_ohe"],
    dropLast=True
)
assembler_r = VectorAssembler(
    inputCols=[
        "humidity_imp", "pressure_imp", "wind_speed_kmh",
        "cloud_cover_pct", "temperature_morning", "dew_point_imp",
        "season_ohe", "region_ohe"
    ],
    outputCol="features",
    handleInvalid="skip"
)
scaler_r = StandardScaler(inputCol="features", outputCol="features_scaled", withMean=True, withStd=True)

preprocessing_r = Pipeline(stages=[
    imputer_r, season_idx_r, region_idx_r, ohe_r, assembler_r, scaler_r
])

multi_eval_acc = MulticlassClassificationEvaluator(
    labelCol="will_rain", predictionCol="prediction", metricName="accuracy"
)
multi_eval_f1 = MulticlassClassificationEvaluator(
    labelCol="will_rain", predictionCol="prediction", metricName="f1"
)
classification_results = {}

print("LogisticRegression")
lr_clf = LogisticRegression(
    featuresCol="features_scaled", labelCol="will_rain",
    maxIter=100, regParam=0.05, family="binomial"
)
pipeline_lr_clf = Pipeline(stages=preprocessing_r.getStages() + [lr_clf])
t0 = time.time()
model_lr_clf = pipeline_lr_clf.fit(train_rain)
elapsed_lr_clf = time.time() - t0
preds_lr_clf = model_lr_clf.transform(test_rain)
acc_lr = multi_eval_acc.evaluate(preds_lr_clf)
f1_lr  = multi_eval_f1.evaluate(preds_lr_clf)
classification_results["LogisticRegression"] = {"Accuracy": acc_lr, "F1": f1_lr, "temps": elapsed_lr_clf}
print(f"  Accuracy : {acc_lr:.4f}  |  F1 : {f1_lr:.4f}  |  Temps : {elapsed_lr_clf:.2f}s")

print("RandomForestClassifier")
rf_clf = RandomForestClassifier(
    featuresCol="features_scaled", labelCol="will_rain",
    numTrees=100, maxDepth=8, seed=42
)
pipeline_rf_clf = Pipeline(stages=preprocessing_r.getStages() + [rf_clf])
t0 = time.time()
model_rf_clf = pipeline_rf_clf.fit(train_rain)
elapsed_rf_clf = time.time() - t0
preds_rf_clf = model_rf_clf.transform(test_rain)
acc_rf = multi_eval_acc.evaluate(preds_rf_clf)
f1_rf  = multi_eval_f1.evaluate(preds_rf_clf)
classification_results["RandomForest"] = {"Accuracy": acc_rf, "F1": f1_rf, "temps": elapsed_rf_clf}
print(f"  Accuracy : {acc_rf:.4f}  |  F1 : {f1_rf:.4f}  |  Temps : {elapsed_rf_clf:.2f}s")

print("GBTClassifier")
gbt_clf = GBTClassifier(
    featuresCol="features_scaled", labelCol="will_rain",
    maxIter=50, stepSize=0.1, maxDepth=5, seed=42
)
pipeline_gbt_clf = Pipeline(stages=preprocessing_r.getStages() + [gbt_clf])
t0 = time.time()
model_gbt_clf = pipeline_gbt_clf.fit(train_rain)
elapsed_gbt_clf = time.time() - t0
preds_gbt_clf = model_gbt_clf.transform(test_rain)
acc_gbt = multi_eval_acc.evaluate(preds_gbt_clf)
f1_gbt  = multi_eval_f1.evaluate(preds_gbt_clf)
classification_results["GBT"] = {"Accuracy": acc_gbt, "F1": f1_gbt, "temps": elapsed_gbt_clf}
print(f"  Accuracy : {acc_gbt:.4f}  |  F1 : {f1_gbt:.4f}  |  Temps : {elapsed_gbt_clf:.2f}s")

best_clf_name = max(classification_results, key=lambda x: classification_results[x]["F1"])
print(f"Matrice de confusion — {best_clf_name}")
preds_map = {
    "LogisticRegression": preds_lr_clf,
    "RandomForest": preds_rf_clf,
    "GBT": preds_gbt_clf
}
preds_map[best_clf_name] \
    .groupBy("will_rain", "prediction") \
    .count() \
    .orderBy("will_rain", "prediction") \
    .show()

print("Tableau récapitulatif classification :")

for mname, metrics in classification_results.items():
    print(f"  {mname:<25} {metrics['Accuracy']:>10.4f} {metrics['F1']:>8.4f} "
          f"{metrics['temps']:>10.2f}")

spark.stop()