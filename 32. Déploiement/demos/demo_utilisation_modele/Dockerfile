# FROM python:3.11.9-slim

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY api_modele.py .

# # Télécharger le modèle au build
# RUN python -c "from transformers import pipeline; \
# pipeline(
#     'sentiment-analysis',
#     model='distilbert-base-uncased-finetuned-sst-2-english'
# )"

# EXPOSE 5000

# ENTRYPOINT ["python", "api_modele.py"]

# Dockerfile optimized
# Stage 1 : Builder
FROM python:3.11.9-slim as builder

WORKDIR /build

COPY requirements.txt .

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

# Télécharger le modèle au build
RUN python -c "from transformers import pipeline; \
pipeline('sentiment-analysis', \
    model='distilbert-base-uncased-finetuned-sst-2-english')"

# Stage 2 : runtime
FROM python:3.11.9-slim

WORKDIR /app

# Copier le venv depuis le builder
COPY --from=builder /opt/venv /opt/venv

# Copier le cache hugging face
COPY --from=builder /root/.cache/huggingface /root/.cache/huggingface 

COPY api_modele.py .

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 5000

ENTRYPOINT ["python", "api_modele.py"]