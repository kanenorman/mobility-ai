FROM python:3.10

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy code base
COPY data_streaming/kafka_producer .

# Specify the command to run when the container starts
CMD ["python", "producer.py"]
