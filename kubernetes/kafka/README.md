# Kafka

Apache Kafka is an open-source distributed event streaming platform used by thousands of companies for high-performance data pipelines, streaming analytics, data integration, and mission-critical applications.

To integrate a Kafka broker with Kerberos vault you could install your existing Kafka installation, or on board a new Kafka broker inside your Kubernetes cluster. Before installing the Kafka broker, we will need to set up a storage class. As previously mentioned we will use OpenEBS for that, but you could use the storage class you prefer.

    kubectl apply -f https://openebs.github.io/charts/openebs-operator.yaml

Once OpenEBS is installed and configured, go ahead with setting up the Kafka broker.

    git clone https://github.com/kerberos-io/vault && cd vault/kubernetes/kafka
    kubectl create namespace kafka
    helm install kafka bitnami/kafka -f values.yaml -n kafka

Once done you should see the relevant kafka pods and zookeeper being deployed

    kubectl get po -n kafka

Now you are ready to configure the Kerberos Vault integration, by selecting the Kafka option. You should add the Kafka credentials and authentication mechanism.
