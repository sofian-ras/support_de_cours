from contextlib import asynccontextmanager

import pandas as pd
from fastapi import Body, FastAPI, HTTPException

from api.model_loader import ModelLoader
from api.schemas import PredictionRequest, PredictionResponse


model_loader = ModelLoader()


def get_risk(probability):
	if probability < 0.2:
		return "LOW", "Aucune action requise"
	if probability < 0.5:
		return "MEDIUM", "Planifier une inspection préventive"
	if probability < 0.75:
		return "HIGH", "Inspection dans les 24h"
	return "CRITICAL", "Arrêt immédiat recommandé"


@asynccontextmanager
async def lifespan(app: FastAPI):
	app.state.metrics = {"total_predictions": 0, "failure_predictions": 0}
	try:
		model_loader.load()
	except Exception:
		pass
	yield


app = FastAPI(title="Predictive Maintenance API", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health():
	return {
		"status": "ok",
		"model_loaded": model_loader.is_loaded,
		"model_version": model_loader.version,
	}


@app.get("/metrics")
def metrics():
	total = app.state.metrics["total_predictions"]
	failures = app.state.metrics["failure_predictions"]
	failure_rate = failures / total if total > 0 else 0.0
	return {
		"total_predictions": total,
		"failure_predictions": failures,
		"failure_rate": failure_rate,
	}


def _to_frame(payload: PredictionRequest):
	return pd.DataFrame([payload.model_dump()])


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest):
	if not model_loader.is_loaded:
		raise HTTPException(status_code=503, detail="Model is not loaded")

	X = _to_frame(payload)
	prediction = int(model_loader.predict(X)[0])
	probability = float(model_loader.predict_proba(X)[0][1])
	risk_level, action = get_risk(probability)

	app.state.metrics["total_predictions"] += 1
	app.state.metrics["failure_predictions"] += prediction

	return PredictionResponse(
		prediction=prediction,
		probability=probability,
		risk_level=risk_level,
		recommended_action=action,
		model_version=model_loader.version,
	)


@app.post("/predict/batch", response_model=list[PredictionResponse])
def predict_batch(payloads: list[PredictionRequest] = Body(max_length=100)):
	if not model_loader.is_loaded:
		raise HTTPException(status_code=503, detail="Model is not loaded")

	X = pd.DataFrame([item.model_dump() for item in payloads])
	preds = model_loader.predict(X)
	probas = model_loader.predict_proba(X)[:, 1]

	outputs = []
	for prediction, probability in zip(preds, probas):
		pred_int = int(prediction)
		prob_float = float(probability)
		risk_level, action = get_risk(prob_float)

		app.state.metrics["total_predictions"] += 1
		app.state.metrics["failure_predictions"] += pred_int

		outputs.append(
			PredictionResponse(
				prediction=pred_int,
				probability=prob_float,
				risk_level=risk_level,
				recommended_action=action,
				model_version=model_loader.version,
			)
		)

	return outputs
