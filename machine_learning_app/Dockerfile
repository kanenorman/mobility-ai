# Use the official Python 3.10 image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the content of the machine_learning directory into the /app directory inside the container
COPY . .

# Install pip requirements
# NOTE: We'll need to create a requirements.txt for this step to work
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for GCP authentication
ENV GOOGLE_APPLICATION_CREDENTIALS /app/service-account-file.json

# Command to run when the container starts
# This is just an example. Modify based on what you want to run as default.
#CMD ["python", "your-main-script.py"]
