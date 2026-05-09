# Build-Kontext = Repo-Root, damit COPY wiki/ funktioniert.
# Aufruf via railway.toml: dockerfilePath=service/Dockerfile, buildContext=.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    WIKI_ROOT=/app/wiki

RUN apt-get update && apt-get install -y --no-install-recommends \
        ripgrep \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# uv für schnelle Installation
RUN pip install uv

# Dependencies separat, damit der Layer cached
COPY service/pyproject.toml /app/service/pyproject.toml
RUN cd /app/service && uv pip install --system --no-cache .

# App-Code
COPY service/app /app/app

# Wiki – wird beim Build mit eingefroren
COPY wiki /app/wiki

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
