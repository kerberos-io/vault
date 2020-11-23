# Kafka handler

The purpose of this exercise will cover following steps:

1. Setup a Kafka broker,
2. Connect Kerberos Storage to Kafka,
3. Retrieve and process real-time messages,
4. Fetch related recording from Kerberos Storage API.
5. Execute a color detection algorithm.

By doing this exercise you have to make sure you have a running kubernetes (k8s) cluster and properly setup [Kerberos Enterprise](https://doc.kerberos.io/enterprise/installation) and [Kerberos Storage](https://doc.kerberos.io/storage/installation).

After installation make sure you have connected on or more cameras to Kerberos Enterprise and have one or more providers (Azure, AWS, GCP or Minio) connected to Kerberos Storage.

Ok.. Let's go!

![Let's go](https://memegenerator.net/img/instances/84132439/lets-go.jpg)

## 1. Setup a Kafka broker

Installing a Kafka broker is easy. At least it's easy for people who are familiar with Helm. Go ahead and install the Kafka helm chart using following command.

    helm repo add bitnami https://charts.bitnami.com/bitnami
    helm install --name kafka bitnami/kafka  -f ./kafka/values.yaml

The `kafka/values.yaml` file contains all the different configurations for your Kafka Broker: username and password, replication factory, number of workers etc. You might need to finetune this for your specific usecase.

Once properly installed you should be able to open a Kafka client (e.g. Kafka Tool), and add the different credentials (Bootstrap servers) and JAAS config.

    org.apache.kafka.common.security.plain.PlainLoginModule required username="aaa" password="xxx";

## 2. Connect Kerberos Storage to Kafka

Making the assumption you have successfully setup your Kafka broker, we can now update our Kerberos Storage installation. Open the Kerberos Storage web interface, and select the queue tab. Add a new queue, select Kafka and fill-in the different settings.

![Kerberos Storage Kafka Configuration](kerberos-storage-kafka.png)

Once saved, all files being uploaded to the Kerberos Storage provider will trigger a message to be send to the Kafka broker and more specifically the topic you've defined (kcloud-event-queue, in above example).

## 3. Retrieve and process real-time messages with Python

A lot of different SDK's and libraries are available for interacting with Kafka brokers (C++, .NET, Golang, Python, PHP, etc). However for simplicity we will use Python.

      from mqueue import CreateQueue

      kafkaQueue = CreateQueue(queueName='kerberos-storage-example-queue',
                               broker='broker1.kerberos.io:9094,broker2.kerberos.io:9094,broker3.kerberos.io:9094',
                               mechanism='PLAIN',
                               security='SASL_PLAINTEXT',
                               username= 'aaa',
                               password='xxx')
      while True:
          try:
              messages = kafkaQueue.ReceiveMessages()
              for message in messages:
                  body = message
                  print message
                  print("next..")
              print("reading..")

          except Exception as e:
              print("error..")
              print(e)
              pass

When running this code `python index.py`, it will continously read from the specified Kafka topic. Each time a recording is uploaded to Kerberos Storage, an event will be generated within a few milliseconds. For example:

    next..
    reading..
    {u'date': 1606164482, u'source': u'gcp-europe-west1', u'payload': {u'fileSize': 305956, u'key': u'vessosa/1606164482_6-818812_FundoEsquerda_229-153-288-247_51_745.mp4', u'metadata': {u'capture': u'IPCamera', u'uploadtime': u'1606164482', u'event-token': u'0', u'event-microseconds': u'0', u'event-numberofchanges': u'51', u'event-instancename': u'FundoEsquerda', u'event-timestamp': u'1606164482', u'publickey': u'AQER!@$214m2154125!TFsdgdsddb325@#%', u'event-regioncoordinates': u'229-153-288-247', u'productid': u'zdrPvi7pwxiWBWBpvvAI6il3fL'}}, u'events': [u'monitor', u'sequence', u'analysis', u'throttler', u'notification'], u'provider': u'kstorage'}
    next..
    reading..
    {u'date': 1606164579, u'source': u'gcp-europe-west1', u'payload': {u'fileSize': 2334417, u'key': u'cedricve/1606164579_6-427681_side_200-200-400-400_24_551.mp4', u'metadata': {u'uploadtime': u'1606164579', u'event-token': u'0', u'event-microseconds': u'0', u'event-numberofchanges': u'24', u'event-instancename': u'side', u'event-timestamp': u'1606164579', u'publickey': u'AQER!@$214m2154125!TFsdgdsddb325@#%', u'event-regioncoordinates': u'200-200-400-400', u'productid': u'qOjUUiPksm3cLqldChp2s6Y1e2LBmj'}}, u'events': [u'monitor', u'sequence', u'analysis', u'throttler', u'notification'], u'provider': u'kstorage'}
    next..
    reading..
    reading..

Each message contains the filename of the recording but also some metadata: timestamp, provider name (source), number of changes pixels (event-numberofchanges), etc.
