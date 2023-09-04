FROM apache/spark:3.3.3-scala2.12-java11-python3-r-ubuntu

WORKDIR /app

COPY requirements.txt .

# change users to install needed packages
ARG spark_uid=185
USER 0
RUN chown ${spark_uid} -R /opt/spark
RUN curl https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.3.3/spark-sql-kafka-0-10_2.12-3.3.3.jar --output /opt/spark/jars/spark-sql-kafka-0-10_2.12-3.3.3.jar
RUN curl https://jdbc.postgresql.org/download/postgresql-42.6.0.jar --output /opt/spark/jars/postgresql-42.6.0.jar
RUN curl https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.5.0/kafka-clients-3.5.0.jar --output /opt/spark/jars/kafka-clients-3.5.0.jar
RUN python3 -m pip install --user -r requirements.txt
USER ${spark_uid}

COPY data_streaming/kafka_consumer /app/data_streaming/kafka_consumer

WORKDIR /app/data_streaming/kafka_consumer


CMD ["/opt/spark/bin/spark-submit", "--master", "local", "--jars", "/opt/spark/jars/spark-sql-kafka-0-10_2.12-3.3.3.jar,/opt/spark/jars/postgresql-42.6.0.jar,/opt/spark/jars/kafka-clients-3.5.0.jar", "consumer.py"]



