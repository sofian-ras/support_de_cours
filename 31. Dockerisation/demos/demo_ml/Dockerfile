FROM python:3.11.9-slim

WORKDIR /app

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le script
COPY train_simple.py .

# Exécuter le script
# CMD ["python", "train_simple.py"]
ENTRYPOINT ["python", "train_simple.py"]