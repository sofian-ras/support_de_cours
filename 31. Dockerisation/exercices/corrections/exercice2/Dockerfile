FROM python:3.11.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p models

COPY wine_data.csv train_model.py .

ENTRYPOINT ["python", "train_model.py"]