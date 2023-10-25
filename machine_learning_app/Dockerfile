# Use the official Python 3.10 image
FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for GCP authentication - set your own path here
# if ran locally 
ENV GOOGLE_APPLICATION_CREDENTIALS /app/service-account-file.json

# Command to run when the container starts
#CMD ["python", "your-main-script.py"]
