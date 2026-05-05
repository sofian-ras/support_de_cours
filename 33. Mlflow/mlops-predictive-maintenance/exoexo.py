import pandas as pd

import pandas as pd


def load_raw_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    rename_map = {
        "Type":                    "type",
        "Air temperature [K]":     "air_temperature",
        "Process temperature [K]": "process_temperature",
        "Rotational speed [rpm]":  "rotational_speed",
        "Torque [Nm]":             "torque",
        "Tool wear [min]":         "tool_wear",
        "Machine failure":         "machine_failure",
    }
    df = df.rename(columns=rename_map)

    cols_to_drop = ["UDI", "Product ID", "TWF", "HDF", "PWF", "OSF", "RNF"]
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

    return df