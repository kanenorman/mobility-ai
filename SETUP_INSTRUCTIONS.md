### Local Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/kanenorman/AC215_MBTArrivals-App.git
   cd AC215_MBTArrivals-App
   ```

1. **Request an API Token**:

   - Visit the [MBTA's official site](https://www.mbta.com/developers/v3-api) or the relevant link to get your API token.

1. **Install Docker Engine**

   - Follow the official [installation guide](https://docs.docker.com/engine/install).

1. **Set Up Your Environment**:

   - Create a local `.env` file in the project directory.
   - Populate the `.env` file with necessary configurations, including your MBTA API Token.

   ```bash
   # kafka & zookeeper
   KAFKA_HOST1=broker1
   KAFKA_HOST2=broker2
   KAFKA_HOST3=broker3
   KAFKA_PORT1=9092
   KAFKA_PORT2=19092
   KAFKA_PORT3=29092
   ZOOKEEPER_PORT=2181

   # API keys
   MBTA_API_KEY=<YOUR-API-KEY-HERE>

   # Postgres
   POSTGRES_PORT=5432
   POSTGRES_DB=mbta
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=password
   POSTGRES_HOST=flask_database
   POSTGRES_DRIVER=org.postgresql.Driver

   # pgAdmin (Postgres Web Portal)
   PGADMIN_DEFAULT_EMAIL=postgres@admin.com
   PGADMIN_DEFAULT_PASSWORD=admin

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

   - Create and activate a new Conda environment named `mbta_env` with Python 3.10 and install requirements:
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
   docker-compose down --volumes && docker-compose build && docker-compose up -d
   ```

1. **Access the App**:

   - Open a web browser and navigate to `localhost:5000`

1. **pgAdmin**:

   - If you prefer to interact with Postgres in the browser instead of the command line. You can utilize pgAdmin.
   - Navigate to `localhost:5050`
   - Enter the email and password specified in the `.env` file (i.e. `PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD`)
   - Click Add New Server.
     - Name it whatever you wish.
     - Click the tab that says `Conection`
     - Enter `flask_databsae` as the `Host name/address`
     - Enter the username and password specified in the `.env` file (i.e. `POSTGRES_USER` and `POSTGRES_PASSWORD`)

1. **Kafka Control Center**
   - If you prefer to use the web interface instead of the terminal application. Navigate to `localhost:9021`
