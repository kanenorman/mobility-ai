# Real-Time MBTA Data Streaming and Arrival Time Prediction

[![Python Badge](https://img.shields.io/badge/Python-3776ab?style=for-the-badge&logo=python&logoColor=yellow)](https://www.python.org/)
[![Flask Badge](https://img.shields.io/badge/Flask-5DB036?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PyTorch Badge](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![scikit-learn Badge](https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Apache Spark Badge](https://img.shields.io/badge/Apache_Spark-FFFFFF?style=for-the-badge&logo=apachespark&logoColor=%23E35A1C)](https://spark.apache.org/)
[![Docker Badge](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL Badge](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-000?style=for-the-badge&logo=apachekafka)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

## Project Health

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/kanenorman/AC215_MBTArrivals-App/main.svg)](https://results.pre-commit.ci/latest/github/kanenorman/AC215_MBTArrivals-App/main)

[![Unit Tests](https://github.com/kanenorman/AC215_MBTArrivals-App/actions/workflows/run-unit-test.yml/badge.svg)](https://github.com/kanenorman/AC215_MBTArrivals-App/actions/workflows/run-unit-test.yml)

## Project Introduction

As a regular user of the MBTA transit system during my time at Harvard, particularly relying on the red line at Harvard Station for quick commutes to MIT, I recognized the importance of accurate transit predictions. While the MBTA provides scheduled predictions, there is an opportunity to create our own real-time predictions. This project aims to encompass a comprehensive full-stack Machine Learning engineering workflow. From data engineering and machine learning to DevOps, MLOps, and web development, the project's goal is to develop a real-time streaming dashboard that predicts whether a transit line will arrive on time or experience delays.

## Project Overview

The primary objective of the MBTA Data Streaming and Prediction Project is to leverage data science and engineering to enhance transit prediction accuracy. By combining real-time data streaming and predictive modeling, we aim to create a system that provides users with valuable insights into transit timings. The project involves several key components:

1. **Real-Time Data Streaming**: Gathering real-time data from the MBTA transit system, including information on train schedules, delays, and historical performance.

2. **Data Engineering**: Processing and transforming the collected data to prepare it for use in predictive modeling.

3. **Predictive Modeling**: Developing machine learning models that analyze historical and real-time data to predict whether a transit line will be on time or experience delays.

4. **Real-Time Predicting**: Implementing a streaming pipeline that continuously updates predictions as new data arrives.

5. **Dashboard Development**: Creating a user-friendly web dashboard that displays real-time transit predictions and provides insights into transit line performance.

6. **DevOps and MLOps**: Establishing an effective DevOps workflow to automate deployment and monitoring of the streaming pipeline and models.

![image](./assets/high-level.svg)

## Project Goals

- Develop accurate predictive models for MBTA transit line timings, integrating both historical and real-time data.
- Implement a data streaming pipeline that continuously updates predictions as new data becomes available.
- Create an interactive web dashboard that enables users to monitor real-time transit predictions.
- Apply DevOps and MLOps practices to ensure automated deployment, scaling, and monitoring of the entire system.

## Technologies Used

- Python
- PySpark
- Kafka
- Machine Learning Libraries (e.g., scikit-learn, TensorFlow)
- Flask (for web dashboard)
- Docker
- GitHub Actions (for CI/CD)

## Project Impact

The MBTA Data Streaming and Prediction Project aims to provide commuters with reliable and accurate transit predictions, enhancing their daily travel experience. By leveraging real-time data and predictive modeling, we hope to contribute to improved transit planning and decision-making for MBTA users.

## Getting Started

To get started with this project, follow the instructions in the project documentation (Coming Soon) to set up the required environment, run the data streaming pipeline, deploy the predictive models, and access the real-time dashboard.

## Feedback

Feedback to this project is always welcome. For feedback or questions, feel free to reach out to me directly.

## Disclaimer

**This Project is for Personal Hobby Use Only**

_This project is developed solely for personal interest and is not intended to be used as a consumer product or as a decision-making tool. It may contain inaccuracies or errors, and there are no guarantees or warranties associated with its use. Users are encouraged to use their discretion and verify any information provided by this project independently._

**Not Affiliated with the MBTA**

_I want to make it explicitly clear that I am not affiliated with the Massachusetts Bay Transportation Authority (MBTA) or any other official transportation organization. This project is independent and unofficial._

_Please exercise caution and use any information or functionality provided by this project responsibly and in accordance with the laws and regulations governing your location._
