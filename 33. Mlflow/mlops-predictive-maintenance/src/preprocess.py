import re

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler


DROP_COLUMNS = {"udi", "product_id", "twf", "hdf", "pwf", "osf", "rnf"}


def _to_snake_case(name: str) -> str:
    name = name.strip().replace("%", "percent")
    name = re.sub(r"[^0-9a-zA-Z]+", "_", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_").lower()


def load_raw_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.rename(columns={col: _to_snake_case(col) for col in df.columns})
    kept_columns = [col for col in df.columns if col not in DROP_COLUMNS]
    return df[kept_columns].copy()


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["temp_delta"] = data["process_temperature_k"] - data["air_temperature_k"]
    data["power_proxy"] = data["rotational_speed_rpm"] * data["torque_nm"]
    data["wear_per_rpm"] = data["tool_wear_min"] / (data["rotational_speed_rpm"] + 1e-6)
    return data


def get_feature_pipeline() -> ColumnTransformer:
    numeric_features = [
        "air_temperature_k",
        "process_temperature_k",
        "rotational_speed_rpm",
        "torque_nm",
        "tool_wear_min",
        "temp_delta",
        "power_proxy",
        "wear_per_rpm",
    ]

    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            (
                "cat",
                OrdinalEncoder(categories=[["L", "M", "H"]], handle_unknown="use_encoded_value", unknown_value=-1),
                ["type"],
            ),
        ]
    )
