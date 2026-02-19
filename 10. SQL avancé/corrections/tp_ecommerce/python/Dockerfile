FROM python:3.12-slim

WORKDIR /app

# psycopg + tzdata (pour les fuseaux horaires via zoneinfo)
RUN pip install --no-cache-dir psycopg[binary] tzdata

COPY report_supershop.py .

CMD ["python", "report_supershop.py"]