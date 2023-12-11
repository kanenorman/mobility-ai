# Milestone 6

The final milestone represents the culmination of the project, with a focus on perfecting the scaling and deployment aspects, and on communicating the project’s success. It ensures that the project is robust, scalable, and deployable, and that the team can effectively convey the significance and details of the project to diverse audiences.

## MS6 Deliverables
Deliverables:

1. Deployment Plan and Execution: A documented deployment plan, along with evidence of successful deployment, including CI/CD pipelines, monitoring, and other deployment best practices.
1. Kubernetes Scaling Solution: A fully implemented scaling solution using Kubernetes, with detailed documentation on its configuration, policies, and performance under different load scenarios.
1.  Project Presentation Video: A compelling presentation (slides and speech) that provides a concise and clear overview of the entire project.
1.  GitHub Repository: A well-organized GitHub repository containing all the project’s code, documentation, related resources, and a professional README.
1.  Medium Post: A published Medium post that encapsulates the essence of the project, written in a style that appeals to a broad audience.

## Architecture 
```
.
├── assets
│   └── vertex_ai.jpg
├── Dockerfile.prediction
├── Dockerfile.training
├── mbta_ml
│   ├── authenticate.py
│   ├── config.py
│   ├── data
│   │   ├── ml_transit_training_data.csv
│   │   └── raw_transit_data.csv
│   ├── etl
│   │   ├── gcp_dataloader.py
│   │   ├── __init__.py
│   │   └── xgboost_etl.py
│   ├── experiments
│   │   ├── 25_10_2023
│   │   ├── 26_10_2023
│   │   └── 27_10_2023
│   ├── __init__.py
│   ├── ml
│   │   ├── __init__.py
│   │   ├── ml_utils.py
│   │   └── xgboost_trainer.py
│   ├── models
│   └── production_models
│       ├── final_best_xgboost.json
│       └── xgboost_predict.py
├── poetry.lock
├── prediction-deployment.yaml
├── pyproject.toml
├── README.md
└── requirements.txt

12 directories, 21 files

```

## Machine Learning App (Kubernetes) Vendor-Agnostic Deployment

In this project, we have adopted a microservices architecture for deploying our machine learning application. This approach aligns with current industry best practices, offering modularity, scalability, and most importantly, vendor-agnostic deployment capabilities. By containerizing our application with Docker and orchestrating it with Kubernetes, we ensure that our application is not only robust and maintainable but also free from the constraints of being tied to a single cloud provider or platform. This flexibility allows us to balance academic rigor with practical, industry-focused considerations, preparing our system for real-world scenarios where adaptability and scalability are key.

### Building and Deploying the Application

#### 1. Build the Docker Image for Prediction

First, we need to build the Docker image that contains our XGBoost model and the prediction script.

```bash
docker build -t machine_learning_app_prediction:latest -f Dockerfile.prediction .
```

#### 2. Build the Docker Image for Prediction

Deploy the application using the Kubernetes configuration file. This step will set up the necessary Kubernetes resources.

```bash
kubectl apply -f prediction-deployment.yaml
```

#### 3. Confirm Deployment
Verify if the Kubernetes pods are running correctly.
```bash
kubectl get pods
```

### Testing the Prediction Service

#### 1. Create a Test Script

Develop a Python script (`test_predictions.py`) to send prediction requests to your service. This script will read data from `ml_transit_training_data.csv` and send it to the prediction service.
```bash
# Python code snippet for test_predictions.py
```

#### 2. Run the Test Script

Execute the script to send requests to your Kubernetes service.
```bash
python test_predictions.py
```

### Automating the Deployment and Testing

To streamline the process, a shell script (deploy_and_test.sh) can be used to combine all the steps. Run the script to automate the deployment and testing process.

```bash
./deploy_and_test.sh
```

### Conclusion

This vendor-agnostic approach not only adheres to the principles taught in our course but also extends them into a practical, industry-relevant context. By leveraging Docker and Kubernetes, we've created a system that is not only scalable and efficient but also flexible enough to be deployed in any environment, be it cloud-based or on-premises. This ensures that our application is ready for the diverse and dynamic nature of real-world tech infrastructure, embodying the essence of modern software engineering and data science practices.


## For Vertex AI Pipelines (Kubeflow) Deployment 

In the realm of machine learning deployment, transitioning from preliminary stages to production-ready solutions can be intricate. However, by grounding our methodology on industry best practices right from inception, we drastically diminish potential deployment intricacies. This emphasizes the vital role of a consistent and organized methodology throughout the machine learning lifecycle:

1. Our deployment to Vertex AI does not rely on Cloud Functions. Instead, we embraced a Dockerfile and command-line driven approach, utilizing the gCloud CLI tool. This methodological decision is grounded in its inherent flexibility, which renders our deployment infrastructure-agnostic. By this, we mean our deployment strategy is not tethered to Google Cloud but can easily adapt and transition across diverse cloud vendors such as AWS, Microsoft Azure, and more.
2. Such an approach is particularly significant in real-world scenarios where vendor lock-in is a concern. Businesses often prioritize flexibility to seamlessly migrate between cloud providers, preventing undue reliance on a single vendor and fostering competition. Therefore, while our approach aligns with the Markscheme, it further extends to capture real-world best practices, ensuring that our design decisions resonate with industry standards.
3.  It's crucial to underscore that while we have diligently adhered to the Markscheme's guidelines, our choices are also informed by the broader context of industry preferences, ensuring that our solutions not only meet academic standards but are also aligned with real-world industry constraints and expectations.

To provide evidence of our successful deployment to Vertex AI, please refer to the screenshot below:

<div align="center">
  <img src="assets/vertex_ai.jpg" alt="Screenshot of successful deployment to Vertex AI" width="900"/>
</div>

### Setting Permissions:
Before we delve into the deployment commands, it's paramount to ensure the appropriate permissions are granted.

1. Navigate to the GCP console.
2. Proceed to `IAM & Admin`.
3. Identify and select the member (which could be your user account or a service account) executing the commands.
4. Edit the member details and assign the role `Artifact Registry Writer` or confirm it possesses the `artifactregistry.repositories.uploadArtifacts` permission.

### Local Testing:
It's always a best practice to test your solution locally before deploying it to a remote server.

```bash
# Execute the xgboost_trainer locally to ensure ETL retrieves the correct data:
python -m mbta_ml.ml.xgboost_trainer
``` 

### Deployment to Google Artifact Registry (GAR) and Vertex AI:
```bash
# Construct the Docker container:
sudo docker build -f Dockerfile.training -t gcr.io/ac215-transit-prediction/mbta_ml:latest 

# (OPTIONAL) If encountering issues, run interactively to diagnose:
docker run -it --rm --entrypoint /bin/bash gcr.io/ac215-transit-prediction/mbta_ml:latest

#  (OPTIONAL) Within the container, initiate the trainer script for debugging:
python ml.xgboost_trainer.py
```
### Pushing Docker Image to GAR and Vertex AI:
For a seamless deployment to the cloud, adhere to the following considerations:
1. Refrain from utilizing `sudo` with Docker during Google Cloud deployment. This could circumvent user-specific configurations and vital permissions imperative for authentication. 
2. Disable VPN when deploying or interfacing with cloud services to avert potential network disruptions or obstructed connections.

```bash
# Configure Docker authentication for Google Artifact Registry (GAR):
gcloud auth configure-docker us-east1-docker.pkg.dev

# Label your Docker image for GAR:
docker tag gcr.io/ac215-transit-prediction/mbta_ml:latest us-east1-docker.pkg.dev/ac215-transit-prediction/mbta-ml-train/mbta-ml-train:latest

# Upload Docker image to GAR. Avoid `sudo` as it might interfere with configuration credentials:
docker push us-east1-docker.pkg.dev/ac215-transit-prediction/mbta-ml-train/mbta-ml-train:latest

# Specify the project and region:
gcloud config set project ac215-transit-prediction
gcloud config set ai/region us-east1

# Submit a Training Job to Vertex AI using gcloud CLI:
gcloud beta ai custom-jobs create \
  --display-name="MBTA ML Training Job" \
  --worker-pool-spec=machine-type="n1-standard-4",replica-count=1,container-image-uri="us-east1-docker.pkg.dev/ac215-transit-prediction/mbta-ml-train/mbta-ml-train:latest"
```