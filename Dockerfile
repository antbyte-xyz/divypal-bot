FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    net-tools iputils-ping dnsutils curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m myuser && \
    mkdir -p /app/data && \
    chown -R myuser:myuser /app

USER myuser

ENV PYTHONUNBUFFERED=1

ENV RES_OPTIONS="attempts:2 retries:2 timeout:1"

CMD ["python", "bot.py"]
