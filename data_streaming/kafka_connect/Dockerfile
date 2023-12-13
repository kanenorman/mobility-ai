FROM confluentinc/cp-kafka-connect:7.5.0

# Create the directory for your custom connectors
RUN mkdir -p /usr/share/confluent-hub-components

# Copy the JDBC connector to the custom connectors directory
COPY ./data_streaming/kafka_streams/kafka-connect-jdbc /usr/share/confluent-hub-components/kafka-connect-jdbc

# Define the command to start Kafka Connect
CMD ["bash", "-c", "echo 'Launching Kafka Connect worker'; /etc/confluent/docker/run"]
