# Kerberos Vault on Kubernetes

As described in the `docker` installation, Kerberos Vault and it's required services are running inside containers. Due to the nature of `docker` and `docker-compose` it's straight forward to setup Kerberos Vault in a few minutes. Using `docker` will give you a fast ramp-up, but will not provide you with a scalable and resilience deployment.

To overcome this and make Kerberos Vault scale and flexible, it's recommended to setup Kerberos Vault in a Kubernetes cluster.