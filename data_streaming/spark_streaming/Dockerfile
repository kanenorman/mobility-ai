# Define base image
FROM bitnami/spark:3.3.3

# Set the working directory
WORKDIR /app

COPY requirements.txt .
RUN pip install -r  requirements.txt

# Copy application code
COPY data_streaming/spark_streaming /app/data_streaming/spark_streaming

# Set the working directory for the application
WORKDIR /app/data_streaming/spark_streaming

# Define the command to run the Spark application
CMD ["spark-submit", \
     "--master", "local", \
     "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.3,org.postgresql:postgresql:42.6.0,org.datasyslab:geotools-wrapper:1.4.0-28.2", \
     "ml_stream.py"]
