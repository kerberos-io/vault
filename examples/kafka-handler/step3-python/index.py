from mqueue import CreateQueue

kafkaQueue = CreateQueue(queueName='kerberos-storage-example-queue',
                         broker='broker0.kerberos.io:9094,broker1.kerberos.io:9094,broker2.kerberos.io:9094',
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
