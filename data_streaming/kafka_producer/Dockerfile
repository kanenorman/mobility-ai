FROM python:3.10

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir producer

# Copy code base
COPY data_streaming/kafka_producer kafka_producer/

# Specify the command to run when the container starts
CMD ["python", "-m", "kafka_producer.producer"]
