# Milestone 4 

## MLOps: Serverless Microservice Architecture

Our machine learning application is meticulously architected using a serverless microservice pattern, proving advantageous in various aspects that empower contemporary application deployment and management standards. Let’s dive deep into its design intricacies:

### Why Serverless?

Serverless architecture is more than a buzzword; it's a strategic choice we made to optimize operational overhead. When deploying applications in traditional architectures, one has to be cautious about provisioning, maintaining, and scaling the servers. Serverless abstracts these concerns, letting us focus on the code and its functionality rather than infrastructural challenges.

- **Seamless Deployment and Scaling**: With serverless, deploying our services becomes as simple as pushing the code. As the traffic to our service grows, serverless platforms automatically scale up our application, and when the traffic subsides, they scale it down. This elastic nature ensures optimal resource utilization without manual intervention.
- **Cost-Efficiency**: In serverless models, we only pay for the compute time our code is running. This can lead to substantial cost savings, especially for applications with fluctuating traffic.

### Modular Microservice Design:

The adoption of a microservice structure for our machine learning application ensures that different components of our application are isolated, modular, and loosely coupled. This modularization offers numerous benefits:

- **Independent Scalability**: Each service can be scaled independently based on its demand, ensuring efficient resource allocation. For instance, if our `xgboost_trainer.py` experiences a higher computational demand, it can be scaled independently without affecting other components.
- **Enhanced Code Management**: With modular services, each service can be developed, tested, and deployed independently. This isolation means bugs in one service won't spill over to another, leading to easier debugging and maintenance.
- **Flexibility in Tech Stack**: Different services can be written in different programming languages or use different data storage techniques. This flexibility ensures that the technology stack is always the best fit for the service's purpose.

### Breaking Down the Directory Structure:

- **Dockerfile.training**: This contains instructions to package our training environment into a container. Using containers ensures consistency across different stages of the application lifecycle, from development to production.
- **mbta_ml**:
    - **authenticate.py**: Centralized authentication service. Keeping this separate ensures secure and consistent access controls across services.
    - **config.py**: Global configurations ensuring all modules remain in sync with system-wide parameters.
    - **data**: Raw and processed datasets reside here, ensuring a clear separation between raw input and feature-engineered data.
    - **dl**: Deep learning specific tasks, making it straightforward to identify and manage neural network-based operations.
    - **etl**: Stands for Extract, Transform, Load. All data preparation, cleaning, and transformation tasks are handled here, ensuring data integrity and quality.
    - **experiments**: Organized by date, this directory holds various experiment outcomes, making it easier to track and compare model performances over time.
    - **ml**: Traditional machine learning tasks and utilities are isolated here, ensuring clarity between deep learning and traditional ML tasks.
    - **models**: Intermediate model artifacts, including weights and structures, are stored here, providing a historical view of model iterations.
    - **production_models**: Houses the final, production-ready models. This separation ensures quick access to deployable artifacts.
    - **pyproject.toml & poetry.lock**: Dependency management, ensuring consistency across environments.
    - **README.md**: Documentation, an essential aspect to provide insights into the system's design and functionality.
    - **test_import.py**: Ensures module imports are functioning correctly.

### Design Rationale:

1. **Production-Grade Training**: By segregating ETL processes, traditional ML, and deep learning, we ensure that any changes or upgrades to the training algorithms don't hamper the data preparation stages and vice-versa. This separation is crucial for maintaining data integrity and model consistency.
2. **Optimized Inference**: The clear demarcation between models and production_models ensures that only the most optimized and tested models are deployed for inference, ensuring efficient resource utilization and rapid response times.

Moreover, it's worth noting that while our current deliverable utilizes the XGBoost model, the flexibility of our architecture accommodates the seamless integration and deployment of deep learning models or any other machine learning algorithms. This flexibility assures that our system remains future-proof, catering to evolving requirements without necessitating substantial overhauls. In essence, the design blueprint shown below ensures that our application remains agile, scalable, maintainable, and robust, striking a balance between innovation and stability. Leading well to our deployments in MS5 and MS6 which are nearly complete.

```
➜  machine_learning_app 
.
├── Dockerfile.training
└── mbta_ml
    ├── authenticate.py
    ├── config.py
    ├── data
    │   ├── ml_transit_training_data.csv
    │   └── raw_transit_data.csv
    ├── dl
    │   ├── dnn_pruner.py
    │   ├── dnn_trainer.py
    │   ├── __init__.py
    │   └── knowledge_distiller.py
    ├── etl
    │   ├── gcp_dataloader.py
    │   └── xgboost_etl.py
    ├── experiments
    ├── __init__.py
    ├── ml
    │   ├── __init__.py
    │   ├── ml_utils.py
    │   └── xgboost_trainer.py
    ├── models
    ├── poetry.lock
    ├── production_models
    │   └── final_best_xgboost.json
    ├── pyproject.toml
    ├── README.md
```
## Addressing the Markscheme

- **Distillation/Quantization/Compression**: 
    - Implemented knowledge distillation to transfer information from a complex model (teacher) to a simpler model (student).
    - Weight and neuron pruning techniques were applied for model optimization to ensure efficient deployment in constrained environments.
    - Refer to `compress_teacher.py` for weight and neuron pruning and `distill_student.py` for knowledge distillation.

- **Vertex AI Pipelines (Kubeflow) and Cloud Functions Integration**:
    - Incorporated Vertex AI Pipelines for orchestrating machine learning workflows.
    - Integrated cloud functions to automate various processes, aligning with best cloud-native practices.

## Best of Practice

By segregating our back-end data engineering, Flask app, and machine learning app, we follow the best industry practices. This modular structure allows for better maintainability, scalability, and independent feature enhancements.

## Tools and Libraries

- **WandB (Weights and Biases)**: Utilized for serverless performance tracking, enabling us to visualize metrics, compare experiments, and share insights.
- **Ray**: Employed for hyperparameter tuning and experiment tracking. It offers the ability to scale and distribute model training across CPU and GPU resources.

## Files and Code Overview

- `delay_etl.py`: 
    - Preprocesses MBTA data.
    - Features: date derivation, encoding categoricals, computing delays and distances, hex value computation, and data cleaning.

- `gcp_dataoader.py`:
    - Authenticates GCP.
    - Extracts MBTA data from BigQuery.
    - Handles NaNs and converts data types.

- `ml_train.py`:
    - Computes evaluation metrics.
    - Trains XGBoost model on MBTA data.
    - Hyperparameter optimization and retraining with best hyperparameters.

- `compress_teacher.py`:
    - Performs weight and neuron pruning on the model.
    - Fine-tunes pruned models.
    - Evaluates and selects the best pruned model.

- `DNN_train_base.py`:
    - Trains a DNN model on MBTA data.
    - Hyperparameter optimization for the DNN model.

- `Distill_student.py`:
    - Creates a student model.
    - Distills knowledge from the teacher model.
    - Hyperparameter optimization for the student model.

**Note**: For comprehensive code details, delve into the respective Python files provided in the application structure.