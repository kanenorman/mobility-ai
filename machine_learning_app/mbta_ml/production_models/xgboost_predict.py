""" xgboost_predict.py
This script is the entry point for making predictions in our Kubernetes deployment.
It is designed to be used within Docker containers as part of a microservice architecture.
The script sets up a Flask web server to handle prediction requests, loading the
XGBoost model for inference. This setup is intended for deployment scenarios where
the model is served in a scalable and distributed manner.
"""
import xgboost as xgb
import pandas as pd
from flask import Flask, request, jsonify
from pathlib import Path

app = Flask(__name__)

# Determine the path to the model file relative to this script
model_path = Path(__file__).parent / "final_best_xgboost.json"

# Load the model from the specified path
model = xgb.XGBRegressor()
model.load_model(str(model_path))

@app.route('/predict', methods=['POST'])
def predict():
    """Predict the response for a single observation.

    :param: None, but expects a JSON payload with model features in a POST request.
    :return: JSON response containing the model's prediction.
    """
    # Extract data from POST request and convert to DataFrame
    data = request.get_json(force=True)
    df = pd.DataFrame(data, index=[0])

    # Make predictions using the loaded model
    predictions = model.predict(df)

    # Return predictions as a JSON response
    return jsonify(predictions.tolist())

if __name__ == '__main__':
    # Run the Flask app on port 80, accessible from outside the container
    app.run(host='0.0.0.0', port=80)
