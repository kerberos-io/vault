from mqueue import CreateQueue
import requests
import cv2
import os
import numpy as np
from sklearn.cluster import KMeans

# Kafka settings
Uri = os.getenv("STORAGE_URI", "https://api.storage.kerberos.io")
AccessKey = os.getenv("STORAGE_ACCESS_KEY", "xx")
SecretAccessKey = os.getenv("STORAGE_SECRET", "xx")

# Kafka settings
QueueName = os.getenv("KAFKA_QUEUE_NAME", "kerberos-storage-example-queue")
Group = os.getenv("KAFKA_GROUP", "group")
Broker = os.getenv("KAFKA_BROKER", "kafka-0:9092")
Mechanism = os.getenv("KAFKA_MECHANISM", "PLAIN")
Security = os.getenv("KAFKA_SECURITY", "SASL_PLAINTEXT")
Username = os.getenv("KAFKA_USERNAME", "xx")
Password = os.getenv("KAFKA_PASSWORD", "xx")

kafkaQueue = CreateQueue(queueName=QueueName,
                         group=Group,
                         broker=Broker,
                         mechanism=Mechanism,
                         security=Security,
                         username= Username,
                         password=Password)

def calculateHistogram(img):

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
    clt = KMeans(n_clusters=3)
    clt.fit(img)

    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    rgbs = []
    for cluster in clt.cluster_centers_:
        rgbs.append(list(map(int,cluster)))
    return rgbs

while True:
    try:
        messages = kafkaQueue.ReceiveMessages()
        for message in messages:

            print(message)
            fileName = message['payload']['key']
            provider = message['source']

            response = requests.get(
                Uri + '/storage/blob',
                headers={
                    'X-Kerberos-Storage-FileName': fileName,
                    'X-Kerberos-Storage-Provider': provider,
                    'X-Kerberos-Storage-AccessKey': AccessKey,
                    'X-Kerberos-Storage-SecretAccessKey': SecretAccessKey,
                },
            )

            if response.status_code != 200:
                print("Something went wrong: " + response.content)
                continue

            fileContent = response.content
            with open('video.mp4', 'wb') as file:
                file.write(fileContent)

            vidcap = cv2.VideoCapture('video.mp4')
            success, img = vidcap.read()

            histogram = []
            if success:
                histogram = calculateHistogram(img)
            else:
                print("Something went wrong while capturing a frame from video.mp4")
            print(histogram)

            print("next..")

        print("reading..")

    except Exception as e:
        print("error..")
        print(e)
        pass
