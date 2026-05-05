import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

from src.preprocess import get_feature_pipeline


def _dataset():
	X_num, y = make_classification(
		n_samples=1000,
		n_features=5,
		n_informative=4,
		n_redundant=0,
		weights=[0.8, 0.2],
		class_sep=1.2,
		random_state=42,
	)

	df = pd.DataFrame(
		{
			"type": np.where(np.arange(len(y)) % 3 == 0, "L", np.where(np.arange(len(y)) % 3 == 1, "M", "H")),
			"air_temperature_k": 295 + X_num[:, 0] * 2,
			"process_temperature_k": 305 + X_num[:, 1] * 2,
			"rotational_speed_rpm": np.clip(1500 + X_num[:, 2] * 200, 0, None),
			"torque_nm": np.clip(40 + X_num[:, 3] * 5, 0, None),
			"tool_wear_min": np.clip(50 + X_num[:, 4] * 10, 0, None),
		}
	)
	df["temp_delta"] = df["process_temperature_k"] - df["air_temperature_k"]
	df["power_proxy"] = df["rotational_speed_rpm"] * df["torque_nm"]
	df["wear_per_rpm"] = df["tool_wear_min"] / (df["rotational_speed_rpm"] + 1e-6)

	return train_test_split(df, y, test_size=0.25, random_state=42, stratify=y)


def _fitted_pipeline():
	X_train, X_test, y_train, y_test = _dataset()
	pipeline = Pipeline(
		steps=[
			("preprocessor", get_feature_pipeline()),
			("smote", SMOTE(random_state=42)),
			("clf", RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42)),
		]
	)
	pipeline.fit(X_train, y_train)
	return pipeline, X_test, y_test


def test_probabilities_in_valid_range():
	model, X_test, _ = _fitted_pipeline()
	proba = model.predict_proba(X_test)[:, 1]
	assert np.all((proba >= 0.0) & (proba <= 1.0))


def test_predictions_are_binary():
	model, X_test, _ = _fitted_pipeline()
	preds = model.predict(X_test)
	assert set(np.unique(preds)).issubset({0, 1})


def test_model_is_not_trivial():
	model, X_test, _ = _fitted_pipeline()
	preds = model.predict(X_test)
	assert len(np.unique(preds)) > 1


def test_deterministic_predictions():
	model, X_test, _ = _fitted_pipeline()
	preds_1 = model.predict(X_test)
	preds_2 = model.predict(X_test)
	assert np.array_equal(preds_1, preds_2)


def test_recall_above_threshold():
	model, X_test, y_test = _fitted_pipeline()
	preds = model.predict(X_test)
	recall = recall_score(y_test, preds)
	assert recall >= 0.3


def test_roc_auc_above_threshold():
	model, X_test, y_test = _fitted_pipeline()
	proba = model.predict_proba(X_test)[:, 1]
	roc_auc = roc_auc_score(y_test, proba)
	assert roc_auc >= 0.55
