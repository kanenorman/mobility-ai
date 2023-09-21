# Data Streaming

## Overview

This README provides a comprehensive overview of our data streaming procedure, utilized to retrieve and store data from the MBTA API. The process involves streaming data from the [MBTA API using the Server Sent Event protocol](https://www.mbta.com/developers/v3-api/streaming), capturing the JSON response, and subsequently forwarding this data to a Kafka topic. A consumer application actively monitors this Kafka topic and is responsible for writing the data into a PostgreSQL database.

![image](../assets/data-streaming.svg)

## Data Streaming Workflow

### 1. Continuous Data Retrieval

The data streaming process commences with a request to the MBTA API. This request is facilitated through a script that performs HTTP requests to the relevant MBTA API endpoints, supplying the necessary API credentials and parameters. The data retrieved from the API is presented in JSON format.

### 2. Kafka Producer

Upon obtaining the JSON data from the MBTA API, it is dispatched to a Kafka topic. The Kafka producer is responsible for disseminating this data to the topic. The Kafka producer can be configured to manage various aspects, including message serialization, error handling, and partitioning strategies.

### 3. Kafka Topic

The Kafka topic serves as a buffer for incoming data. Kafka topics enable the decoupling of data producers and consumers, ensuring that data remains accessible for consumption even if the consumer experiences temporary downtime.

### 4. Kafka Consumer

A Kafka consumer application actively listens to the Kafka topic, consuming incoming data as it arrives. Once received, the consumer processes the data using Apache Spark, preparing it for storage in PostgreSQL.

### 5. PostgreSQL Database

The processed data is subsequently written to a PostgreSQL database. The consumer application interfaces with the database, performing tasks such as data visualization and facilitating machine learning predictions.
