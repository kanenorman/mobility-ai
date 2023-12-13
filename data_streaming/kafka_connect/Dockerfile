FROM confluentinc/cp-kafka-connect:7.5.0

# Create the directory for your custom connectors
RUN mkdir -p /usr/share/confluent-hub-components

# Copy the JDBC connector to the custom connectors directory
COPY ./data_streaming/kafka_streams/kafka-connect-jdbc /usr/share/confluent-hub-components/kafka-connect-jdbc

# Install the JDBC connector using Confluent Hub
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-jdbc:10.7.4

# Define the command to start Kafka Connect
CMD ["bash", "-c", "echo 'Launching Kafka Connect worker'; /etc/confluent/docker/run"]
