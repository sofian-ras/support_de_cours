import numpy as np
import pandas as pd

from src.preprocess import add_engineered_features, get_feature_pipeline, load_raw_data


def _raw_dataframe() -> pd.DataFrame:
	return pd.DataFrame(
		{
			"UDI": [1, 2, 3],
			"Product ID": ["M1", "M2", "M3"],
			"Type": ["L", "M", "H"],
			"Air temperature [K]": [295.0, 300.0, 305.0],
			"Process temperature [K]": [305.0, 311.0, 317.0],
			"Rotational speed [rpm]": [0.0, 1500.0, 2500.0],
			"Torque [Nm]": [30.0, 35.0, 40.0],
			"Tool wear [min]": [5.0, 10.0, 15.0],
			"Machine failure": [0, 1, 0],
			"TWF": [0, 0, 0],
			"HDF": [0, 0, 0],
			"PWF": [0, 0, 0],
			"OSF": [0, 0, 0],
			"RNF": [0, 0, 0],
		}
	)


def _prepared_features() -> pd.DataFrame:
	raw = _raw_dataframe().rename(
		columns={
			"Type": "type",
			"Air temperature [K]": "air_temperature_k",
			"Process temperature [K]": "process_temperature_k",
			"Rotational speed [rpm]": "rotational_speed_rpm",
			"Torque [Nm]": "torque_nm",
			"Tool wear [min]": "tool_wear_min",
			"Machine failure": "machine_failure",
		}
	)
	return add_engineered_features(raw).drop(columns=["machine_failure", "UDI", "Product ID", "TWF", "HDF", "PWF", "OSF", "RNF"], errors="ignore")


def test_pipeline_fit_transform_shape(tmp_path):
	csv_path = tmp_path / "ai4i.csv"
	_raw_dataframe().to_csv(csv_path, index=False)
	loaded = load_raw_data(str(csv_path))
	engineered = add_engineered_features(loaded)
	X = engineered.drop(columns=["machine_failure"])

	pipeline = get_feature_pipeline()
	transformed = pipeline.fit_transform(X)

	assert transformed.shape[0] == X.shape[0]


def test_numeric_features_are_scaled():
	X = _prepared_features()
	pipeline = get_feature_pipeline()
	transformed = pipeline.fit_transform(X)

	numeric_block = transformed[:, :8]
	means = np.mean(numeric_block, axis=0)
	assert np.all(np.abs(means) < 1e-7)


def test_categorical_encoding():
	X = _prepared_features()
	pipeline = get_feature_pipeline()
	transformed = pipeline.fit_transform(X)
	cat_col = transformed[:, -1]
	assert np.array_equal(cat_col, np.array([0.0, 1.0, 2.0]))


def test_temp_delta_computed():
	df = _prepared_features()
	expected = df["process_temperature_k"] - df["air_temperature_k"]
	assert np.allclose(df["temp_delta"], expected)


def test_wear_per_rpm_no_division_by_zero():
	df = _prepared_features()
	values = df["wear_per_rpm"].to_numpy()
	assert np.isfinite(values).all()


def test_original_df_not_mutated():
	original = _prepared_features().drop(columns=["temp_delta", "power_proxy", "wear_per_rpm"])
	snapshot = original.copy(deep=True)
	_ = add_engineered_features(original)
	pd.testing.assert_frame_equal(original, snapshot)
