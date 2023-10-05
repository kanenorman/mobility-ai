# AC215 - Milestone2

**Table of Contents**
- [Team Members](#team-members)
- [Group Name](#group-name)
- [Project](#project)
- [Micro Service Descriptions](#micro-service-descriptions)
  - [Zookeeper](#zookeeper)
  - [Broker1, Broker2, Broker3](#brokers)
  - [Schema-Registry](#schema-registry)
  - [Control-Center](#control-center)
  - [Producer](#producer)
  - [Consumer](#consumer)
  - [Flask App](#flask-app)
  - [Flask Database](#flask-database)
- [Project Organization](#project-organization)
- [Running Locally](#running-locally)

**Team Members**
Kane Norman, Juan Castillo, Philip Ndikum, David Wintermeyer

**Group Name**
MBTArrivals

**Project**
Amidst growing difficulties in urban mobility and the need for timely transit predictions, our
group project aims to build a scalable time series forecasting system for the Massachusetts
Bay Transportation Authority (MBTA) transit system. By combining modern data engineering and scalable Machine Learning operations (MLOps) methodologies, this research aims to address pressing challenges in infrastructure and transit reliability -- with broader implications for supply-chain optimization and logistics. By providing guidelines and solutions, our project serves as an instructive blueprint, and a substantive contribution to the ever-growing data engineering and urban mobility literature.

### Micro Service Descriptions

In this project, we implement a microservice architecture where each service is containerized using Docker
and orchestrated via a `docker-compose.yml` file. Here's an overview of the services:

#### Zookeeper

Zookeeper is a crucial distributed coordination service that plays a vital role in managing distributed systems.
In this project, it is primarily utilized within the Apache Kafka ecosystem for tasks such as maintaining configuration information,
ensuring distributed synchronization, and providing a naming service.

#### Broker1, Broker2, Broker3

Brokers serve as the backbone of a Kafka infrastructure. They are responsible for receiving messages from producers,
securely storing these messages, and efficiently delivering them to consumers. We employ multiple broker instances within our Kafka cluster for redundancy
to ensure fault tolerance and scalability -- enhancing the robustness of our system.

#### Schema-Registry

The Schema Registry service is integral to our data pipeline, enabling the storage and management of Avro schemas
associated with Kafka topics. Its primary function is to ensure data consistency and compatibility between producers and consumers --
facilitating the seamless exchange of information within our architecture.

#### Control-Center

The Control Center is an indispensable tool for managing and monitoring Apache Kafka clusters.
It provides valuable insights into the health and performance of our Kafka infrastructure, helping us maintain a
resilient and responsive messaging system.

#### Producer

The Producer service is responsible for generating and dispatching messages to Kafka topics.
Its primary data source is the [mbta-v3-api](https://www.mbta.com/developers/v3-api), which supports real-time data streaming
through Server Sent Events (SSE). This service is pivotal in ensuring that fresh data is continuously ingested into our system.
The bulk of this code can be found in the `/data_streaming/kafka_producer` directory.

#### Consumer

The Consumer service plays a vital role in processing messages from Kafka topics. It leverages the power of
[Spark Structured Streaming](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html)
to efficiently extract and process data from Kafka. This enables us to perform complex data transformations and analytics,
driving our data-driven decision-making processes.
The bulk of this code can be found in the `/data_streaming/kafka_consumer` directory.

#### Flask App

Our Flask App is the user-facing component of our system, built using the Flask web framework.
We employ Flask's Jinja2 templating framework for the frontend, while Bluma CSS handles our CSS styling.
This combination ensures an interactive and visually appealing web interface for our users, enhancing their overall experience.
The bulk of this code can be found in the `/flask_app/app` directory.

#### Flask Database

The Flask Database service is a PostgreSQL database at the core of our data storage and retrieval system.
To facilitate spatial data processing, we have integrated the PostGIS extension into our database.
This extension enables us to handle spatial data effectively, a critical requirement for our predictive models and geospatial applications.
The bulk of this code can be found in the `/postgres` and `/flask_app/app/views` directories.

In the future, once our model is developed, we will make an API endpoint for the model and run it as a separate microservice.

## Project Organization

```
├── assets
│   ├── data-streaming.svg
│   └── high-level.svg
├── data_streaming
│   ├── kafka_consumer
│   │   ├── consumer.py
│   │   ├── Dockerfile
│   │   ├── __init__.py
│   │   ├── schemas
│   │   │   ├── alerts.py
│   │   │   ├── __init__.py
│   │   │   ├── schedules.py
│   │   │   ├── shapes.py
│   │   │   ├── stops.py
│   │   │   ├── trips.py
│   │   │   └── vehicles.py
│   │   └── utils
│   │       ├── config.py
│   │       ├── __init__.py
│   │       └── spark_functions.py
│   ├── kafka_producer
│   │   ├── config.py
│   │   ├── Dockerfile
│   │   ├── __init__.py
│   │   ├── producer.py
│   │   └── tests
│   │       ├── __init__.py
│   └── README.md
├── dev-requirements.txt
├── docker-compose.yml
├── flask_app
│   ├── app
│   │   ├── config
│   │   │   ├── config.py
│   │   │   ├── __init__.py
│   │   ├── extensions.py
│   │   ├── __init__.py
│   │   ├── models
│   │   │   ├── alert.py
│   │   │   ├── __init__.py
│   │   │   ├── schedule.py
│   │   │   ├── shape.py
│   │   │   ├── stop.py
│   │   │   ├── trip.py
│   │   │   └── vehicle.py
│   │   ├── static
│   │   │   ├── images
│   │   │   │   └── train-icon.png
│   │   │   └── js
│   │   │       ├── index.js
│   │   │       └── stops.js
│   │   ├── templates
│   │   │   └── index.html
│   │   └── views.py
│   └── Dockerfile
├── LICENSE
├── milestone_submissions
│   └── milestone2
│       └── README.md
├── postgres
│   ├── db
│   │   └── init.sql
│   └── Dockerfile
├── pytest.ini
├── README.md
└── requirements.txt
```

### Running Locally

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/kanenorman/AC215_MBTArrivals-App.git
    cd AC215_MBTArrivals-App
    ```

1. **Request an API Token**:
   - Visit the [MBTA's official site](https://www.mbta.com/developers/v3-api) or the relevant link to get your API token.

1. **Set Up Your Environment**:
   - Create a local `.env` file in the project directory.
   - Populate the `.env` file with necessary configurations, including your MBTA API Token.

   ** Example: `.env` file **
   This section lists the configuration variables used in the project along with  corresponding values.
   ```bash
    # kafka & zookeeper
    KAFKA_HOST1=broker1
    KAFKA_PORT1=9092
    KAFKA_HOST2=broker2
    KAFKA_PORT2=19092
    KAFKA_HOST3=broker3
    KAFKA_PORT3=29092
    ZOOKEEPER_PORT=2181
    SCHEDULES_INPUT_TOPIC=mbta-schedules-input

    # API keys
    MBTA_API_KEY= [Your_key]

    # Postgres
    POSTGRES_PORT=5432
    POSTGRES_DB=mbta
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=password
    POSTGRES_HOST=flask_database
    POSTGRES_DRIVER=org.postgresql.Driver
    POSTGRES_TABLE=schedule

    # Flask
    FLASK_PORT=5000
   ```

1. **Set up Python Version using Pyenv**:
    - If you haven't installed `pyenv` yet, you can do so by following the instructions on [pyenv's GitHub repository](https://github.com/pyenv/pyenv#installation).
    - Install the required Python version:
        ```bash
        pyenv install 3.10.0
        pyenv local 3.10.0
        ```
    - Verify the activated Python version:
        ```bash
        python --version
        ```

1. **Set up and Activate Conda Environment**:
    - Create and activate a new Conda environment named "mbta_env" with Python 3.10 and install requirements:
        ```bash
        conda config --add channels conda-forge # Ensure extra channels added
        conda create --name mbta_env python=3.10
        conda activate mbta_env
        pip install -r requirements.txt
        ```

1. **Ensure Docker is Running (For Docker Users)**:
    ```bash
    sudo systemctl start docker
    sudo systemctl status docker
    ```

1. **Run the App with Docker**:
    ```bash
    docker-compose up -d
    ```

1. **Access the App**:
   - Open a web browser and navigate to `localhost:5000`.
