import numpy as np
import pytest
from fastapi.testclient import TestClient

from api import main


class FakeModelLoader:
	def __init__(self):
		self.is_loaded = True
		self.version = "test-version"

	def load(self):
		return None

	def predict(self, X):
		return np.array([1] * len(X))

	def predict_proba(self, X):
		return np.array([[0.2, 0.8]] * len(X))


@pytest.fixture
def client(monkeypatch):
	fake = FakeModelLoader()
	monkeypatch.setattr(main, "model_loader", fake)
	with TestClient(main.app) as test_client:
		test_client.app.state.metrics = {"total_predictions": 0, "failure_predictions": 0}
		yield test_client


def _valid_payload() -> dict:
	return {
		"type": "M",
		"air_temperature_k": 300.0,
		"process_temperature_k": 310.0,
		"rotational_speed_rpm": 1600.0,
		"torque_nm": 40.0,
		"tool_wear_min": 60.0,
	}


def test_health_returns_200(client):
	response = client.get("/health")
	assert response.status_code == 200


def test_predict_returns_200(client):
	response = client.post("/predict", json=_valid_payload())
	assert response.status_code == 200


def test_predict_response_schema(client):
	response = client.post("/predict", json=_valid_payload())
	data = response.json()
	expected = {"prediction", "probability", "risk_level", "recommended_action", "model_version"}
	assert expected.issubset(data.keys())


def test_predict_probability_range(client):
	response = client.post("/predict", json=_valid_payload())
	probability = response.json()["probability"]
	assert 0.0 <= probability <= 1.0


def test_invalid_type_returns_422(client):
	payload = _valid_payload()
	payload["type"] = "X"
	response = client.post("/predict", json=payload)
	assert response.status_code == 422


def test_temperature_out_of_range_returns_422(client):
	payload = _valid_payload()
	payload["air_temperature_k"] = 120.0
	response = client.post("/predict", json=payload)
	assert response.status_code == 422


def test_batch_max_100(client):
	payload = [_valid_payload() for _ in range(101)]
	response = client.post("/predict/batch", json=payload)
	assert response.status_code == 422


def test_metrics_increments_after_predict(client):
	initial = client.get("/metrics").json()
	assert initial["total_predictions"] == 0

	client.post("/predict", json=_valid_payload())
	after = client.get("/metrics").json()

	assert after["total_predictions"] == 1
	assert after["failure_predictions"] == 1
