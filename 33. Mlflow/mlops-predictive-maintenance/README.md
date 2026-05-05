# MLOps Predictive Maintenance

TP complet de maintenance prédictive basé sur AI4I 2020 : preprocessing, entraînement avec MLflow, serving FastAPI, tests et conteneurisation Docker.

## Structure

```
mlops-predictive-maintenance/
├── data/
│   └── ai4i2020.csv
├── src/
│   ├── preprocess.py
│   └── train.py
├── api/
│   ├── main.py
│   ├── schemas.py
│   └── model_loader.py
├── tests/
│   ├── test_preprocess.py
│   ├── test_model.py
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Installation locale

```bash
pip install -r requirements.txt
```

## Entraînement

Lancer MLflow (si besoin):

```bash
mlflow server --host 0.0.0.0 --port 5000
```

Puis entraîner le modèle:

```bash
python src/train.py
```

## API

```bash
uvicorn api.main:app --reload
```

Endpoints principaux:

- `GET /health`
- `GET /metrics`
- `POST /predict`
- `POST /predict/batch`

## Tests

```bash
pytest --cov=src --cov=api --cov-report=term-missing
```

## Docker Compose

```bash
docker compose up --build
```

Services:

- `mlflow` sur `http://localhost:5000`
- `api` sur `http://localhost:8000`
- `trainer` one-shot pour lancer `python src/train.py`
