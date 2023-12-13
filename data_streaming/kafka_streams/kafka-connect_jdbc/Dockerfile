FROM curlimages/curl:8.4.0

# Copy the JDBC connector to a directory in the container
COPY ./data_streaming/kafka_streams/kafka-connect-jdbc /etc/kafka_streams/kafka-connect-jdbc

# Set the working directory to the location of the JDBC connector
WORKDIR /etc/kafka_streams/kafka-connect-jdbc

# Run your build_connectors.sh script
CMD ["./build_connectors.sh"]
