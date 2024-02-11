from kafka import KafkaProducer
from json import dumps

class Kafkaproducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: dumps(x).encode('utf-8'))

    def error_callback(self, exception):
        raise Exception('Error while sending data to kafka: {0}'.format(str(exception)))

    def write_to_kafka(self, topic_name, input, output):
        print("Sending: ", output, input)
        
        self.producer.send(topic=topic_name, value={'input': input, 'output': output}).add_errback(self.error_callback)
        
        # Flush the producer to ensure all messages are sent
        self.producer.flush()
        print("Wrote message into topic: {0}".format(topic_name))