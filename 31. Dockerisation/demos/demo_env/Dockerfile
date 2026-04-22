FROM python:3.11.9-slim

WORKDIR /app

COPY hello.py .

# definir les variables d'environnement par défaut
ENV NOM="invité" AGE="0"

ENTRYPOINT [ "python", "hello.py" ]