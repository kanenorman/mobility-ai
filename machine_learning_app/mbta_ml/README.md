# MBTA Machine Learning Application

This repository contains the production-grade codebase for the deployment of out MBTA Machine & Deep Learning Applications.  Note: The original codebase was primarily developed using Google Cloud notebooks. This repository is an effort to convert that code into a more modular and production-ready format, and it might be subjected to further refactorings.

```
machine_learning_app
│
├── config.py # Configuration file containing paths, constants, and environment variables
│
├── dl # Deep Learning related scripts
│   ├── dnn_pruner.py # Script for pruning deep neural networks
│   ├── dnn_trainer.py # Script for training deep neural networks
│   └── knowledge_distiller.py # Knowledge distillation logic for compressing DNNs
│
├── Dockerfile # Dockerfile to containerize the application
│
├── etl # Data extraction, transformation, and loading scripts
│   ├── delay_etl.py # ETL script for MBTA delay data
│   └── gcp_dataloader.py # Script for loading data from Google Cloud Platform
│
├── ml # Traditional machine learning scripts
│   └── xgboost_trainer.py # Script for training models using XGBoost
│
├── requirements.txt # Project dependencies and their versions
│
├── setup.py # Script for setting up the application
│
└── utils.py # Utility functions and helper scripts
```
## Next Steps

### Milestone 4:

1. Refactor the existing code for production readiness.
1. Test the application locally ensuring all modules run as expected.
1. Containerize the application using the provided Dockerfile.
1. Deploy the Docker container on Google Vertex AI for training.

### Milestone 6:
1. Scale out the application by deploying it to Kubernetes.
1. Monitor, evaluate, and optimize the deployment for better resource utilization.
