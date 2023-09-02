FROM python:3.10

WORKDIR /app

COPY requirements.txt .
COPY data_streaming/kafka_producer .

RUN python -m pip install -r requirements.txt

CMD ["python", "producer.py"]
