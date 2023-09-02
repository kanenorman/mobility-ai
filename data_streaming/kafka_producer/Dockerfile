# Use the official Apache Spark base image as a starting point
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy all necessary files from your local directory to the container
COPY . .

# Install the Python dependencies
RUN python -m pip install -r requirements.txt

# Run the Python script as the container's entry point
CMD ["python", "producer.py"]
