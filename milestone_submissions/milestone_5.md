# Milestone 5

## Project Organization

```
.
├── assets
│   ├── architecture
│   │   ├── kafka-producer.svg
│   │   └── kafka-stream.svg
│   └── figures
│       ├── data-streaming.svg
│       ├── high-level.svg
│       ├── mobility_ai_logo.png
│       ├── wanddb_monitoring.pdf
│       └── wanddb_monitoring.png
├── data_streaming
│   ├── kafka_producer
│   │   ├── config.py
│   │   ├── Dockerfile
│   │   ├── __init__.py
│   │   ├── producer.py
│   │   └── README.md
│   ├── kafka_streams
│   │   ├── kafka-connect-jdbc
│   │   │   └── build_connectors.sh
│   │   ├── ksqldb-server
│   │   │   └── queries.sql
│   │   └── README.md
│   └── README.md
├── dev-requirements.txt
├── docker-compose.yml
├── flask_app
│   ├── app
│   │   ├── config
│   │   │   ├── config.py
│   │   │   ├── __init__.py
│   │   │   └── __pycache__
│   │   │       ├── config.cpython-310.pyc
│   │   │       └── __init__.cpython-310.pyc
│   │   ├── extensions.py
│   │   ├── __init__.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── location.py
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-310.pyc
│   │   │   │   ├── location.cpython-310.pyc
│   │   │   │   ├── route.cpython-310.pyc
│   │   │   │   ├── schedule.cpython-310.pyc
│   │   │   │   ├── scheduled_arrival.cpython-310.pyc
│   │   │   │   ├── stop.cpython-310.pyc
│   │   │   │   └── trip.cpython-310.pyc
│   │   │   ├── route.py
│   │   │   ├── scheduled_arrival.py
│   │   │   ├── schedule.py
│   │   │   ├── stop.py
│   │   │   ├── trip.py
│   │   │   └── vehicle.py
│   │   ├── __pycache__
│   │   │   ├── extensions.cpython-310.pyc
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   └── views.cpython-310.pyc
│   │   ├── static
│   │   │   ├── about.txt
│   │   │   ├── android-chrome-192x192.png
│   │   │   ├── android-chrome-512x512.png
│   │   │   ├── apple-touch-icon.png
│   │   │   ├── css
│   │   │   │   └── styles.css
│   │   │   ├── favicon-16x16.png
│   │   │   ├── favicon-32x32.png
│   │   │   ├── favicon.ico
│   │   │   ├── images
│   │   │   │   ├── mobility_ai_logo.png
│   │   │   │   └── train-icon.png
│   │   │   ├── js
│   │   │   │   ├── index.js
│   │   │   │   └── stops.js
│   │   │   └── site.webmanifest
│   │   ├── templates
│   │   │   ├── about.html
│   │   │   ├── base.html
│   │   │   ├── copyright.html
│   │   │   ├── index.html
│   │   │   ├── navigation.html
│   │   │   └── terms.html
│   │   └── views.py
│   └── Dockerfile
├── LICENSE
├── machine_learning_app
│   ├── assets
│   │   └── vertex_ai.jpg
│   ├── Dockerfile.training
│   ├── mbta_ml
│   │   ├── authenticate.py
│   │   ├── config.py
│   │   ├── data
│   │   │   ├── ml_transit_training_data.csv
│   │   │   └── raw_transit_data.csv
│   │   ├── etl
│   │   │   ├── gcp_dataloader.py
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   ├── delay_etl.cpython-311.pyc
│   │   │   │   ├── gcp_dataloader.cpython-311.pyc
│   │   │   │   ├── __init__.cpython-311.pyc
│   │   │   │   └── xgboost_etl.cpython-311.pyc
│   │   │   └── xgboost_etl.py
│   │   ├── experiments
│   │   │   ├── 25_10_2023
│   │   │   ├── 26_10_2023
│   │   │   └── 27_10_2023
│   │   ├── __init__.py
│   │   ├── ml
│   │   │   ├── __init__.py
│   │   │   ├── ml_utils.py
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-310.pyc
│   │   │   │   ├── __init__.cpython-311.pyc
│   │   │   │   ├── ml_utils.cpython-311.pyc
│   │   │   │   ├── xgboost_trainer.cpython-310.pyc
│   │   │   │   └── xgboost_trainer.cpython-311.pyc
│   │   │   └── xgboost_trainer.py
│   │   ├── models
│   │   ├── production_models
│   │   │   └── final_best_xgboost.json
│   │   └── __pycache__
│   │       ├── authenticate.cpython-310.pyc
│   │       ├── authenticate.cpython-311.pyc
│   │       ├── config.cpython-310.pyc
│   │       ├── config.cpython-311.pyc
│   │       ├── __init__.cpython-310.pyc
│   │       ├── __init__.cpython-311.pyc
│   │       └── test_import.cpython-311.pyc
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── README.md
│   └── requirements.txt
├── milestone_submissions
│   ├── README.md
│   └── vertex_ai.jpg
├── postgres
│   ├── db
│   │   └── init.sql
│   └── Dockerfile
├── pytest.ini
├── README.md
├── requirements.txt
├── SETUP_INSTRUCTIONS.md
└── tests
    ├── __init__.py
    └── kafka_producer_configs_test.py
```

## App Design, Setup, and Code Organization

![High Level Architecture](../assets/figures/high-level.svg)

We adopted a microservices-based approach for modularity and future scalability. Our code organization is meticulously structured, promoting ease of maintenance and clarity. Docker and Docker Compose are pivotal in maintaining consistency across various deployment stages. 
- **Kafka Producer**: We implemented a Kafka Producer to initiate data ingestion, channeling data streams efficiently to the Kafka Message Brokers.
- **Kafka Message Broker**: This serves as the backbone of our architecture, adeptly managing data flow between components, ensuring both robustness and scalability.
- **Data Processing to PostgreSQL**: We process and store data in a PostgreSQL database, ensuring effective data management and retrieval capabilities.
- **FlaskSQLAlchemy Integration**: By integrating FlaskSQLAlchemy, we facilitate seamless interaction between our Flask applications and the PostgreSQL database.
- **Flask with MapBox and Google Client**: Our Flask application is enriched with dynamic data visualization tools like MapBox and Google Client, enhancing user interaction on the frontend.
- **FastAPI for Model Serving**: We employ FastAPI to expose our XGBoost model via a RESTful API, ensuring streamlined communication across services.
- **XGBoost Model on Google Vertex AI**: Hosted on Google Vertex AI, our XGBoost model benefits from Kubernetes-powered autoscaling and efficient model serving.
- **API Development**: We focused on developing robust APIs using FastAPI and Flask, ensuring effective backend-frontend communication.
- **Frontend Design**: Our frontend is designed to be intuitive and responsive, integrated seamlessly with backend APIs for real-time data interactions.
- **User Interface**: The integration of MapBox and Google Client offers users an interactive and informative experience.

## Deployment Strategy and CI/CD

- **GitHub Actions & GitHub for CI/CD**: Contrary to using Ansible, we leveraged GitHub Actions and GitHub for our Continuous Integration and Continuous Deployment pipeline. This choice allowed us to automate our software development processes, from testing to deployment, within the GitHub ecosystem.
- **GCP Deployment**: We deployed our application on Google Cloud Platform, utilizing its robust and scalable infrastructure.
- **Streamlined Deployment Process**: Our CI/CD pipeline ensures consistent and efficient deployment, enabling us to swiftly roll out updates and improvements.

Our `docker-compose.yml` contains all the instructions required to deploy our application:

- **Zookeeper Service**: Uses the `confluentinc/cp-zookeeper:7.5.0` image, with the specified port and environment variables. It includes a health check using nc (netcat).
- **Kafka Brokers (broker1, broker2, broker3)**: Each broker uses the `confluentinc/cp-kafka:7.5.0` image. They are configured with individual broker IDs, Zookeeper connection settings, listener settings, and health checks. They depend on the Zookeeper service being healthy.
- **Schema Registry**: Utilizes the `confluentinc/cp-schema-registry:7.5.0` image and depends on the Kafka brokers and Kafka Connect service (`connect`) being healthy. It exposes port 8081 and is configured with environment variables for Kafka and schema registry settings.
- **Kafka Connect**: Based on `confluentinc/cp-kafka-connect:7.5.0`, this service depends on the Kafka brokers and a `flask_database` service. It exposes port 8083 and includes various Kafka Connect configurations, a volume mount for Kafka Connect JDBC, and a health check.
- **Sink Connectors**: Uses the `curlimages/curl:8.4.0` image, depending on `flask_database` and `connect`. It runs a script for building connectors.
- **Control Center**: Utilizes `confluentinc/cp-enterprise-control-center:7.5.0`, depending on Kafka brokers and `ksqldb-server`. It exposes port 9021 and is configured with various environment variables related to Kafka, Connect, KSQL, and schema registry.
- **Producer**: A custom service built from a Dockerfile in `./data_streaming/kafka_producer/Dockerfile`. It depends on Kafka brokers and includes environment variables for Kafka and an API key.
- **KSQLDB Server and CLI**: Both use Confluent's ksqlDB images (`confluentinc/ksqldb-server:0.29.0` and `confluentinc/ksqldb-cli:0.29.0`). The server exposes port 8088 and is configured with various KSQL settings, including a volume for SQL queries. The CLI depends on the server and Kafka brokers.
- **Flask App**: A custom service built from a Dockerfile in `./flask_app/Dockerfile`. It exposes a specified Flask port and depends on the `flask_database` service. It includes environment variables for database URI and others.
- **Flask Database**: Built from a Dockerfile in `./postgres/Dockerfile`. It exposes a specified PostgreSQL port and is configured with PostgreSQL environment variables. It includes a volume for data persistence and a health check.
- **PgAdmin**: Based on `dpage/pgadmin4`, it depends on the `flask_database` service, exposes port 5050, and is configured with PGAdmin default email and password.
- **The entire deployment is organized within a custom network named `network`**, and a volume named `postgres_data` is defined for database persistence. This setup implies a sophisticated and integrated environment, primarily focused on Kafka-based data processing and management, with Flask serving as the web framework.


## Backend Data Infrastructure to Front Flask App Connections

Our team has meticulously designed and implemented a robust backend-to-frontend infrastructure within our Flask application. This architecture is strategically developed to ensure an efficient and seamless flow of data from Kafka streams to our PostgreSQL database, and ultimately to the frontend UI. Full set-up instructions are shown in `SETUP_INSTRUCTIONS.md`. The following is a detailed summary of the integral components and their specific roles:

- **Models Directory**
  - *Purpose*: Hosts the definitions of our data models, which are directly mapped to database tables via FlaskSQLAlchemy. These models are vital for our data structure and handling.
  - *Key Files*: Comprises location.py, route.py, scheduled_arrival.py, schedule.py, stop.py, trip.py, and vehicle.py.
  - *Functionality*: These models precisely structure the data received from Kafka and stored in our PostgreSQL database, forming the core of our data management strategy.

- **Views.py**
  - *Role*: Central to defining route configurations for our Flask application, acting as a gateway for data requests and responses.
  - *Integration*: Facilitates the interaction between the frontend and our Flask backend. It includes routes for retrieving data from the database, handling updates streamed from Kafka.
  - *Key Functionality*: The index route is pivotal in rendering the homepage with train schedules and stop information, sourced from the database.

- **Extensions.py**
  - *Usage*: Contains the FlaskSQLAlchemy extension, crucial for database operations.
  - *Significance*: This extension is used for all database interactions, making it an essential component of our backend infrastructure.

- **Dockerfile**
  - *Objective*: Outlines the containerization strategy for our Flask application.
  - *Insight*: Provides a clear view of the runtime environment, especially highlighting the use of Python 3.10 and the port exposure for the Flask app.

- **init.py in the App Directory**
  - *Function*: Serves as the entry point for creating and configuring the Flask application.
  - *Features*: Initializes and registers the Flask app, database, and routes. It also sets the app environment and ensures database tables are created at startup.

- **Data Flow Overview**
  - *Kafka to Flask*
    - *Process*: Data ingested by our Kafka producer is sent to Kafka topics, from where it is consumed by our service.
    - *Data Handling*: The consumed data is processed and stored in the PostgreSQL database using the structures defined in our models directory.
  - *Flask to Frontend*
    - *Mechanism*: Data is retrieved from the database through routes in views.py, which then transmit this data to the frontend.
    - *Presentation*: The frontend leverages HTML and JavaScript from the static and templates directories to display the data, ensuring an interactive user interface.


## Conclusion 

We designed our application's architecture with a focus on efficiency, robustness, and scalability, aligning with the markscheme objectives. The integration of technologies like Kafka, Flask, FastAPI, XGBoost, along with the strategic use of Google Cloud Platform and GitHub Actions for CI/CD, underlines our commitment to building a high-performing, scalable, and user-centric application. Our architecture not only meets the markscheme's requirements but is also poised to adapt and evolve with future technological advancements and user needs. In Milestone 6 we will integrate our mlapp with our final backend architecture. 
