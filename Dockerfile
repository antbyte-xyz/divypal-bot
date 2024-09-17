FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m myuser
USER myuser

RUN mkdir -p /app/data && chown -R myuser:myuser /app

ENV PYTHONUNBUFFERED=1

CMD ["python", "bot.py"]