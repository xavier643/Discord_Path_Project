FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app/server

# minimal OS deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && rm -rf /var/lib/apt/lists/*

# copy only server code and its requirements
COPY requirements.txt /app/server/requirements.txt
RUN pip install --no-cache-dir -r /app/server/requirements.txt

# then copy the rest of the server source
COPY . /app/server/

EXPOSE 5000
# You wanted to run from within server, so entry is app.py (no package mode)
CMD ["python", "app.py"]
