FROM apache/spark:3.3.3-scala2.12-java11-python3-r-ubuntu

WORKDIR /app

COPY requirements.txt .

# Use the root user temporarily for installing Python dependencies
USER root

RUN python3 -m pip install --user -r requirements.txt

USER 185

COPY data_streaming/kafka_consumer /app/data_streaming/kafka_consumer

WORKDIR /app/data_streaming/kafka_consumer

CMD ["/opt/spark/bin/spark-submit", "--master", "local", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,org.postgresql:postgresql:42.6.0", "consumer.py"]

