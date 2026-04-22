FROM python:3.11.9-slim

WORKDIR /app

ENV ENVIRONMENT=development
ENV MODEL_TYPE=simple
ENV N_ESTIMATORS=10
ENV LOG_LEVEL=DEBUG
ENV ENABLE_MONITORING=false
ENV DATA_PATH=/app/data/sample.csv
ENV MODEL_OUTPUT=/app/models/dev/

COPY model_trainer.py .

ENTRYPOINT ["python", "model_trainer.py"]