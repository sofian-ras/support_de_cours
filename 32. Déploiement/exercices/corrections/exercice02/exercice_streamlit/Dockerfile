FROM python:3.11.9-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

# Télécharger les modèles au build
RUN python -c "from transformers import pipeline; \
pipeline('summarization', model='facebook/bart-large-cnn'); \
pipeline('translation', model='Helsinki-NLP/opus-mt-en-fr'); \
pipeline('text-classification', model='j-hartmann/emotion-english-distilroberta-base')"

# Stage 2 : runtime
FROM python:3.11.9-slim

WORKDIR /app

# Copier le venv depuis le builder
COPY --from=builder /opt/venv /opt/venv

# Copier le cache hugging face
COPY --from=builder /root/.cache/huggingface /root/.cache/huggingface

COPY app.py .

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 7860

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]