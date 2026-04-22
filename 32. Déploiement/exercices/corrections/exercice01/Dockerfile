FROM python:3.11.9-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

# Télécharger le modèle au build
RUN python -c "from transformers import pipeline; \
pipeline('text-classification', \
    model='papluca/xlm-roberta-base-language-detection')"

# Stage 2 : runtime
FROM python:3.11.9-slim

WORKDIR /app

# Copier le venv depuis le builder
COPY --from=builder /opt/venv /opt/venv

# Copier le cache hugging face
COPY --from=builder /root/.cache/huggingface /root/.cache/huggingface 

COPY app.py .

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

ENTRYPOINT ["python", "app.py"]