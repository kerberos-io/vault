docker build -t kafka-handler .
docker tag kafka-handler kerberos/kafka-handler:1.0
docker push kerberos/kafka-handler:1.0

