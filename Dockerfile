FROM python:3.12-slim

# Dependências do sistema (se precisar, ajuste)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

COPY . .

# Render expõe a variável $PORT automaticamente
ENV PYTHONUNBUFFERED=1
CMD ["bash", "-lc", "gunicorn app:app --bind 0.0.0.0:${PORT:-8000} --workers 3"]
