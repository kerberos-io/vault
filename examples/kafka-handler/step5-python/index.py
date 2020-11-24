from mqueue import CreateQueue
import requests

AccessKey = 'xxx'
SecretAccessKey = 'xxx'

kafkaQueue = CreateQueue(queueName='kerberos-storage-example-queue',
                         broker='kafka-prod0.kerberos.io:9094,kafka-prod1.kerberos.io:9094,kafka-prod2.kerberos.io:9094',
                         mechanism='PLAIN',
                         security='SASL_PLAINTEXT',
                         username= 'aaa',
                         password='xxx')
while True:
    try:
        messages = kafkaQueue.ReceiveMessages()
        for message in messages:

            print(message)
            fileName = message['payload']['key']
            provider = message['source']

            response = requests.get(
                'https://api.storage.kerberos.io/storage/blob',
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

            print("next..")

        print("reading..")

    except Exception as e:
        print("error..")
        print(e)
        pass
