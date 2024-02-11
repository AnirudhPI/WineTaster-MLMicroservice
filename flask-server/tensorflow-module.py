# Import necessary libraries
from json import loads
from flask import Flask
from flask import request
from flask.wrappers import Response
from kafkaclient import KafkaClient
from flask_cors import CORS
import requests
import numpy as np

app = Flask(__name__)
CORS(app)

OUTPUT_LEN = 6
TOPIC_NAME = "ml-model-train"

producer = KafkaClient(TOPIC_NAME)

@app.route("/")
def default():
    return "The Flask app is Working"

# for predictions
@app.route("/predict", methods=['GET', 'POST'])
def predict():
    print("Running prediction")
    print("Request Data:")
    
    data = loads(request.data.decode(encoding="ascii"))
    print(data)

    # construct payload for TensorFlow serving
    raw = "{\"instances\":[["
    for key, value in data.items():
        raw = raw + data[key] + ","
    raw = raw[:-1]  # Remove trailing comma
    raw = raw + "]]}"
    print(raw)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
