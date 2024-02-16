import keras
import numpy as np
import sys
sys.path.append('../')
from flaskserver.kafkaclient import KafkaClient

TOPIC_NAME = "ml-model-train"
BATCH_SIZE = 2
count = 0

consumer = KafkaClient(TOPIC_NAME, mode='consumer')

print("Loading Model v1")
model = keras.models.load_model('saved_model/1')

X, Y = [], []
print("Consuming..")

for message in consumer:
    count += 1
    if not message or not message.value:
        continue

    print("Count: ", count, " Message: ", message.value)

    try: 
        X.append([float(i) for i in message.value['input'].split(',')])
        Y.append([float(i) for i in message.value['output'].split(',')])
    except ValueError as e:
        print(f"Error processing message {message.value}: {e}")
        continue

    if count % BATCH_SIZE == 0:
        print("X: ",X,"\nY: ",Y)
        X=np.array(X)
        Y=np.array(Y)
        model.fit(X,Y, epochs=3)
        if count%(BATCH_SIZE*2) ==0:
            model.save('saved_model/2')
            print("Model Saved")
        X, Y = [], []


