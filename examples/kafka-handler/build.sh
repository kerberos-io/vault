docker build -t kafka-handler .
docker tag kafka-handler kerberos/kafka-handler:1.1
docker push kerberos/kafka-handler:1.1

