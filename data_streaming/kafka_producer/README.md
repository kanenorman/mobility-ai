# Kafka Producer

## Overview

This README provides information about the Kafka producer component of the application pipeline.
The Kafka producer is responsible for publishing data retrieved from the MBTA API to a Kafka topic, serving as a crucial link in the data streaming pipeline.

<div align="center">
  <img src="/assets/architecture/kafka-producer.svg" alt="Kafka Producer" width="700"/>
</div>

## Kafka Producer Workflow

### Data Retrieval

The Kafka producer retrieves real-time data from the MBTA API via [Server Sent Events](https://www.mbta.com/developers/v3-api/streaming).
This data includes train arrival times, statuses, and other relevant transit information.

### Data Publishing

Upon receiving data from the MBTA API, the Kafka producer publishes this data to a specified Kafka topic.
The producer handles the serialization of data and manages any network or data transmission errors.

### Configuration

The Kafka producer can be configured to manage various aspects.
Configuration details are specified in a separate configuration file.

### Documentation

Official MBTA API documentation can be found [here](https://api-v3.mbta.com/docs/swagger/index.html).
