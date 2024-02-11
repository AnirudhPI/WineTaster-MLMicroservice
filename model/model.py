import keras
from keras.backend import dtype
from flaskserver.kafkaclient import KafkaClient

TOPIC_NAME = "ml-model-train"

consumer = KafkaClient(TOPIC_NAME, mode='consumer')

BATCH_SIZE = 2
count = 0


print("Loading Model v1")
model = keras.models.load_model('saved_model/1')

