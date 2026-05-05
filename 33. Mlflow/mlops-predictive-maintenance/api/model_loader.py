import os

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient


class ModelLoader:
	def __init__(self, model_name=None, experiment_name="predictive-maintenance"):
		self.model_name = model_name or os.getenv("MODEL_NAME", "predictive-maintenance-model")
		self.experiment_name = experiment_name
		self._model = None
		self._version = "unknown"

	@property
	def is_loaded(self):
		return self._model is not None

	@property
	def version(self):
		return self._version

	def load(self):
		tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
		mlflow.set_tracking_uri(tracking_uri)

		try:
			uri = f"models:/{self.model_name}/latest"
			self._model = mlflow.sklearn.load_model(uri)
			self._version = "latest"
			return
		except Exception:
			pass

		client = MlflowClient(tracking_uri=tracking_uri)
		experiment = client.get_experiment_by_name(self.experiment_name)
		if experiment is None:
			raise RuntimeError("No MLflow experiment found for fallback model loading")

		runs = client.search_runs(
			experiment_ids=[experiment.experiment_id],
			filter_string="attributes.status = 'FINISHED'",
			order_by=["attributes.start_time DESC"],
			max_results=1,
		)

		if not runs:
			raise RuntimeError("No finished run found for fallback model loading")

		run_id = runs[0].info.run_id
		uri = f"runs:/{run_id}/model"
		self._model = mlflow.sklearn.load_model(uri)
		self._version = run_id

	def predict(self, X):
		if self._model is None:
			raise RuntimeError("Model not loaded")
		return self._model.predict(X)

	def predict_proba(self, X):
		if self._model is None:
			raise RuntimeError("Model not loaded")
		return self._model.predict_proba(X)
