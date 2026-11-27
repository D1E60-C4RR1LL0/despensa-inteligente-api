
FROM python:3.12-alpine@sha256:c5ba3deef00c7758561a0f03c26f44f10589263d40e732b8748e0d1f38f6dd89

RUN apk upgrade --no-cache krb5-libs

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir --only-binary=:all: -r requirements.txt \
    && addgroup -S -g 10001 app \
    && adduser -S -D -H -u 10001 -G app -h /app app \
    && mkdir /data \
    && chown app:app /data

COPY app.py alembic.ini ./
COPY alembic/ ./alembic/
COPY config/ ./config/
COPY models/ ./models/
COPY routes/ ./routes/
COPY schemas/ ./schemas/
COPY utils/ ./utils/

USER app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/openapi.json', timeout=2).close()"]

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
