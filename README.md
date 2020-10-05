# Kerberos Storage

Users or Enteprises which only have a few surveillance cameras to manage, probably will be fine with Kerberos Open Source. On top of that they might include Kerberos Cloud for remote access and monitoring.

On the other hand if you plan to manage a larger network of surveillance cameras, you will have to look into Kerberos Enterprise. Backed up with Kubernetes, Kerberos Enterprise, will give you the real super powers to your scale surveillance camera landscape. Kerberos Enterprise comes with a Front-End to manage and scale your deployments inside a Kubernetes Cluster.

Kerberos Enterprise leverages a service called, Kerberos Storage, for central and hybrid storage. Kerberos Storage implements the concept of BYOC (Bring Your Own Cloud). By selecting a cloud provider (AWS, GCP, AZURE) or on-premise (Minio) you can bring your recordings where you them to be.

In addition to the concept of BYOC, Kerberos Storage enables you to connect to Kerberos Cloud (with your own storage), send events to message brokers (such as Kafka or SQS) and enables you to build custom apps or services (such as a custom machine learning service).

## Installation

For installing Kerberos Storage, you can follow [the how-to on our documentation website](https://doc.kerberos.io/storage/installation). In this repository you will find all the configuration files used in the installation tutorial.
