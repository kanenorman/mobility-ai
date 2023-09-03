FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-traditional

COPY requirements.txt .
COPY data_streaming/kafka_producer .

RUN python -m pip install -r requirements.txt

CMD ["./start_producer.sh"]

