FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY start.sh /app/start.sh
COPY app/main.py .
COPY app/pipeline.py .
COPY app/retrieval.py .
COPY app/llm.py .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT}"]

CMD ["bash", "start.sh"]


