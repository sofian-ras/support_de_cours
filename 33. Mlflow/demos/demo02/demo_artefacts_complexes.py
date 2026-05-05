import mlflow
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json

mlflow.set_experiment("demo-artifacts")

with mlflow.start_run(run_name="complex-artifacts"):
    # 1. CSV
    df = pd.DataFrame({
        "epoch": range(10),
        "loss": np.random.random(10),
        "accuracy": np.random.random(10)
    })

    df.to_csv("metrics.csv")
    mlflow.log_artifact("metrics.csv", "metrics")

    # 2. json
    config = {"lr": 0.01, "batch_size": 32, "epochs": 10}
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    mlflow.log_artifact("config.json")

    # 3. Multiple plots
    fig, axes = plt.subplots(2,2, figsize=(12,10))
    for i, ax in enumerate(axes.flat):
        ax.plot(np.random.random(10))
        ax.set_title(f"metric {i+1}")
    plt.tight_layout()
    plt.savefig("all_metrics.png")
    mlflow.log_artifact("all_metrics.png", "plots")

    print("terminé")