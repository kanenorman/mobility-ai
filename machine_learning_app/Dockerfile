# Use the official Python 3.10 image
FROM python:3.10

# Set the working directory in the container to /mbta_ml
WORKDIR /mbta_ml

# Copy the mbta_ml directory into the container
COPY ./mbta_ml /mbta_ml

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install the mbta_ml package
RUN pip install -e .

# Set the environment variable for GCP authentication (if ran locally)
# Users can override this using Docker's -e flag or use a volume to mount their JSON
ENV GOOGLE_APPLICATION_CREDENTIALS /mbta_ml/service-account-file.json

# Command to run when the container starts (update it when you finalize your main script)
#CMD ["python", "your-main-script.py"]
