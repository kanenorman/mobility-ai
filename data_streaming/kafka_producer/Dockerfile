# Use a Python base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file and Kafka producer code
COPY requirements.txt .
COPY data_streaming/kafka_producer .

# Install Python dependencies
RUN pip install -r requirements.txt

# Specify the command to run when the container starts
CMD ["python", "producer.py"]
