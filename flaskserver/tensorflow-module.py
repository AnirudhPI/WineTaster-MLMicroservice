# Import necessary libraries
from json import loads
from flask import Flask
from flask import request
from flask.wrappers import Response
from kafkaclient import KafkaClient
from flask_cors import CORS, cross_origin
import requests
import numpy as np

app = Flask(__name__)
CORS(app,resources={r"/*": {"origins": ["http://localhost:5500", "http://127.0.0.1:5500"]}})


OUTPUT_LEN = 6
TOPIC_NAME = "ml-model-train"

producer = KafkaClient(TOPIC_NAME)

@app.route("/")
@cross_origin()
def default():
    return "Flask is working"

# for predictions
@app.route("/predict", methods=['GET', 'POST'])
@cross_origin()
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

    url = "http://localhost:8605/v1/models/inc_model:predict"
    headers = {
        'Content-Type': 'text/plain'
    }
    response = requests.request("POST", url, headers=headers, data=raw)
    res_json=response.json()
    print(res_json)
    predictions=np.argmax(np.array(res_json["predictions"][0]))
    print(predictions)

    output={}
    output["prediction"]=int(predictions)+3
    return output

@app.route("/annotate", methods=['GET', 'POST'])
@cross_origin()
def annotate():
    X = []
    Y = []
    csv_x = ""
    csv_y = ""
    print("Request Data:")
    data = loads(request.data.decode(encoding="ascii"))
    print(data)
    for key, value in data.items():
        if key == "quality":
            for i in range(OUTPUT_LEN):
                if i == int(value)-3:
                    csv_y += "1,"
                else:
                    csv_y += "0,"
        else:
            csv_x = csv_x+value+","
    csv_x = csv_x[:-1]  # Remove extra ,
    csv_y = csv_y[:-1]
    return {"message": "Got it"}
    producer.write_to_kafka(csv_x, csv_y)
    return {"message": "Got it"}

if __name__ == "__main__":
    app.run(debug=True, port=5001)
