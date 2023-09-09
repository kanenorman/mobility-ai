# Stage 1: Define base image
FROM apache/spark:3.3.3-scala2.12-java11-python3-r-ubuntu as base

# Set the working directory
WORKDIR /app

COPY requirements.txt .

# Define ARGs for output paths
ARG spark_sql_kafka_jar_output="/opt/spark/jars/spark-sql-kafka-0-10_2.12-3.3.3.jar"
ARG postgresql_jar_output="/opt/spark/jars/postgresql-42.6.0.jar"
ARG kafka_clients_jar_output="/opt/spark/jars/kafka-clients-3.5.0.jar"
ARG spark_token_provider_jar_output="/opt/spark/jars/spark-token-provider-kafka-0-10_2.12-3.3.3.jar"

# Change users to install needed packages
ARG spark_uid=185
USER 0
RUN chown ${spark_uid} -R /opt/spark

# Install additional JAR files and Python packages
RUN curl -L https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.3.3/spark-sql-kafka-0-10_2.12-3.3.3.jar -o ${spark_sql_kafka_jar_output} && \
    curl -L https://jdbc.postgresql.org/download/postgresql-42.6.0.jar -o ${postgresql_jar_output} && \
    curl -L https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.5.0/kafka-clients-3.5.0.jar -o ${kafka_clients_jar_output} && \
    curl -L https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.3.3/spark-token-provider-kafka-0-10_2.12-3.3.3.jar -o ${spark_token_provider_jar_output} && \
    python3 -m pip install --user -r requirements.txt

# Switch back to the spark user
USER ${spark_uid}

# Stage 2: Copy application code
COPY data_streaming/kafka_consumer /app/data_streaming/kafka_consumer

# Set the working directory for the application
WORKDIR /app/data_streaming/kafka_consumer

# Define the command to run the Spark application
CMD ["/opt/spark/bin/spark-submit", \
     "--master", "local", \
     "--jars", "${spark_sql_kafka_jar_output},${postgresql_jar_output},${kafka_clients_jar_output},${spark_token_provider_jar_output}", \
     "consumer.py"]
