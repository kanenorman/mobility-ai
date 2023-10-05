# Milestone 3: Building a Scalable and Modular Computing Infrastructure

## Introduction

This milestone focuses on constructing a robust, scalable, and modular computing infrastructure. With a nod to adaptability, we've created a system that can seamlessly integrate with diverse tools and cloud services. Such a design is imperative in real-world scenarios, ensuring projects are not strictly tethered to a single vendor like Google or Amazon.

## Architecture Highlights

### 1. Distributed Computing and Cloud Storage Integration
1. **Distributed Computing and Cloud Storage Integration**:
    - Google Cloud Platform (GCP) Our primary cloud storage solution. By leveraging GCP, we can use a plethora of tools and services, including Google Colab Pro for expansive experimentation. Whilst wer selected GCP based on the markscheme, we tried to use platform agnostic tools and version controlled our code on Github to ensure our architecture isn't confined to one ecosystem or vendor, reflecting a broad, real-world approach where flexibility and scalability are paramount.
    - Data Pipeline: The design embodies robust extraction, transformation, and versioning capabilities. Examples of versioned datasets underline its effectiveness.
1. **Data Management**: While our current phase primarily harnesses tools outside the TensorFlow ecosystem, our architectural decisions leave the door open for seamless integration with TensorFlow's utilities (like TF Data and TF Records) in future iterations.We have a robust and flexible architecture which allows us to use different libraries and tools and scale out our end-to-end architecture.

##  Machine Learning Workflow Implementation
A detailed exposition of advanced training workflows is provided, complete with evidence of successful training runs, experiment tracking, and avenues for multi-GPU/serverless training.

**Files**:
1. **gcp_dataloader.py**
   - **Purpose**: Extraction and preprocessing of transit data from Google Cloud Platform buckets.
   - **Functions**:
     - `authenticate_gcp()`: Authenticate GCP access.
     - `extract_from_gcp()`: Fetch raw data via SQL.
     - `preprocess_data()`: Data preprocessing functionalities.

2. **delay_etl.py**
   - **Purpose**: Oversees transit data preprocessing for bus delay predictions.
   - **Functions**:
     - `create_date_features()`: Feature engineering specific to dates.
     - `transform()`: ETL tasks tailored for delay data.
     - `data_checks_and_cleaning()`: Data sanitation and cleaning operations.

3. **ml_train.py**
   - **Purpose**: Manages GPU-based training, optimization, assessment, and model serialization.
   - **Functions**:
     - `compute_metrics_table()`: Crafts a metrics table for regression models.
     - `retrain_best_xgboost()`: Post-tuning model retraining via Ray and WandB.
     - `retrain_model_with_best_config()`, `train_mbta()`: Model training utilities.

## Concluding Remarks

Our approach meets all requirements laid out in the Milestone 3 framework. We've forged a resilient and flexible architecture, ensuring we're poised to scale and adapt in forthcoming phases. As we look ahead, the upcoming milestones will see us delving into financial estimations concerning data quality control for the government. We are optimistic that our findings will foster tangible, positive impacts for citizens, extending beyond the confines of this project.
