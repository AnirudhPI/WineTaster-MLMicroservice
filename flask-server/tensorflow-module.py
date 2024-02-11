# Import necessary libraries
from json import loads
from flask import Flask
from flask import request
from flask.wrappers import Response
from kafkaproducer import Kafkaproducer
from flask_cors import CORS
import requests
import numpy as np

app = Flask(__name__)
CORS(app)

OUTPUT_LEN = 6  # Assuming this is the number of possible classes for quality
TOPIC_NAME = "ml-model-train"

producer = Kafkaproducer()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
