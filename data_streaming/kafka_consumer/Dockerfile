# Define base image
FROM bitnami/spark:3.3.3

# Set the working directory
WORKDIR /app

COPY requirements.txt .
RUN pip install -r  requirements.txt

# Copy application code
COPY data_streaming/kafka_consumer /app/data_streaming/kafka_consumer

# Set the working directory for the application
WORKDIR /app/data_streaming/kafka_consumer

# Define the command to run the Spark application
CMD ["spark-submit", \
     "--master", "local", \
     "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.3,org.postgresql:postgresql:42.6.0,org.apache.sedona:sedona-spark-shaded-3.0_2.12:1.4.0,org.datasyslab:geotools-wrapper:1.4.0-28.2", \
     "consumer.py"]
