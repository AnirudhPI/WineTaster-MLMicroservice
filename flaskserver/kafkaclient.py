from kafka import KafkaProducer
from kafka import KafkaConsumer
from json import dumps, loads

class KafkaClient:
    def __init__(self, topic_name=None, mode='producer'):
        self.topic_name = topic_name
        if mode == 'producer':
            self.client = KafkaProducer(
                bootstrap_servers=['localhost:9092'],
                api_version=(0,11,5),
                value_serializer=lambda x: dumps(x).encode('utf-8'))
        elif mode == 'consumer' and topic_name is not None:
            self.client = KafkaConsumer(
                topic_name, 
                bootstrap_servers=['localhost:9092'],
                api_version=(0,11,5),
                value_deserializer=lambda x: loads(x.decode('utf-8')))
        else:
            raise ValueError("Consumer mode requires a topic_name")

    def error_callback(self, exception):
        raise Exception('Error while sending data to kafka: {0}'.format(str(exception)))

    def write_to_kafka(self, input, output):
        if not isinstance(self.client, KafkaProducer):
            raise ValueError("Client is not configured as a producer")
        
        topic_name = self.topic_name if self.topic_name else "default-topic"
        
        print("topic name: ", topic_name)
        print("Sending: ", output, input)
        
        self.client.send(topic=topic_name, value={'input': input, 'output': output}).add_errback(self.error_callback)
        
        # Flush the producer to ensure all messages are sent
        self.client.flush()
        print("Wrote message into topic: {0}".format(topic_name))