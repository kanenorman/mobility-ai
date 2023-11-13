# Kafka Streams

## Overview

This README outlines the purpose and functionality of the Kafka Streams component within our MBTA project. KSQL is used for processing and analyzing the real-time data streamed from the MBTA API, enabling efficient and scalable data manipulation.

<div align="center">
  <img src="/assets/architecture/kafka-stream.svg" alt="Kafka Stream" width="800"/>
</div>

## Kafka Streams Workflow

### Stream Processing

Kafka Streams processes data flowing through Kafka topics. This involves filtering, aggregating, and transforming the data streams in real-time, catering to the specific needs of our application.

### Stateful Operations

The component is capable of performing stateful operations, like windowed computations and join operations, to derive meaningful insights from the streaming data.

### Scalability and Fault Tolerance

Designed for high performance and scalability, Kafka Streams automatically manages stream partitions and ensures fault tolerance through state replication and recovery mechanisms.

### Integration with Other Components

Kafka Streams seamlessly integrates with other components of the project, such as the Kafka producer for data input and the PostgreSQL database for data output.

### Streaming Pattern Convention

#### Bronze Layer

The bronze layer involves ingesting raw topics from the MBTA API. This initial layer captures the data in its most unprocessed form, preserving the original structure and content.

#### Silver Layer

In the silver layer, the topics are flattened and refined. This step involves transforming the raw data, correcting anomalies, and enriching the data to make it more suitable for analysis and querying.

#### Gold Layer

The gold layer is where the most processed and valuable data tables are created. At this stage, data is fully optimized for business intelligence and analytics, providing actionable insights and supporting decision-making processes.

### Sink Connectors to PostgreSQL

Sink connectors are utilized to efficiently transfer data from Kafka Streams to the PostgreSQL database. These connectors automate the process of extracting data from Kafka topics and loading it into PostgreSQL tables, ensuring data consistency and reliability. The connectors are configured to handle schema evolution and updates, providing a seamless integration between our streaming data pipeline and the database.

### Additional Resources

- [Kafka Streams Documentation](https://kafka.apache.org/documentation/streams/)
- [KSQL Documentation](https://docs.confluent.io/platform/current/ksql/docs/index.html)
- [Confluent Kafka Connectors](https://docs.confluent.io/home/connect/overview.html)
