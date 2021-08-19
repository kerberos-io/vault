# Kerberos Vault

Users or Enteprises which only have a few surveillance cameras to manage, probably will be fine with Kerberos Open Source. On top of that they might include Kerberos Hub for remote access and monitoring.

On the other hand if you plan to manage a larger network of surveillance cameras, you will have to look into Kerberos Enterprise. Backed up with Kubernetes, Kerberos Enterprise, will give you the real super powers to your scale surveillance camera landscape. Kerberos Enterprise comes with a Front-End to manage and scale your deployments inside a Kubernetes Cluster.

![arch-kerberos-vault-providers](https://user-images.githubusercontent.com/1546779/130074390-88b61351-96b7-42e4-89ab-ebdb243f1efb.png)

Kerberos Enterprise leverages a service called, Kerberos Vault, for central and hybrid storage. Kerberos Vault implements the concept of BYOC (Bring Your Own Cloud). By selecting a cloud provider (AWS, GCP, AZURE) or on-premise (Minio) you can bring your recordings where you them to be.

In addition to the concept of BYOC, Kerberos Vault enables you to connect to [Kerberos Hub](https://doc.kerberos.io/hub/first-things-first/) (with your own storage), send events to message brokers (such as Kafka or SQS) and enables you to build custom apps or services (such as a custom machine learning service).

## Installation

For installing Kerberos Vault, you can follow [the how-to on our documentation website](https://doc.kerberos.io/vault/installation). In this repository you will find all the configuration files used in the installation tutorial.

## Examples

A couple of [examples can be found here](examples). These examples illustrates how the Kerberos Vault API is working, and how it can be used to develop custom algorithms or applications.
