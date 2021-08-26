import json
from confluent_kafka import Producer, Consumer

def CreateQueue(queueName='', group='', broker='', mechanism='', security='', username= '', password=''):
    return Kafka(queueName=queueName, group=group, broker=broker, mechanism=mechanism, security=security, username=username, password=password)

class Kafka:
    def __init__(self, queueName='', group='', broker='', mechanism='', security='', username= '', password=''):
        self.queueName = queueName
        kafkaC_settings = {
            'bootstrap.servers': broker,
            "group.id":             group,
            "session.timeout.ms":   10000,
            "queued.max.messages.kbytes": 10000, #10MB
        	"auto.offset.reset":    "earliest",
            "sasl.mechanisms":   mechanism,#"PLAIN",
            "security.protocol": security, #"SASL_PLAINTEXT",
            "sasl.username":     username,
            "sasl.password":     password,
        }
        self.kafka_consumer = Consumer(kafkaC_settings)
        self.kafka_consumer.subscribe([self.queueName])

    def ReceiveMessages(self):
        msg = self.kafka_consumer.poll(timeout=1.0)
        if msg is None:
            return []
        return [json.loads(msg.value())]

    def Close(self):
        self.kafka_consumer.close()
        return True
