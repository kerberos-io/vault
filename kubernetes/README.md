# Kerberos Vault on Kubernetes

As described in the `docker` installation, Kerberos Vault and it's required services are running inside containers. Due to the nature of `docker` and `docker-compose` it's straight forward to setup Kerberos Vault in a few minutes. Using `docker` will give you a good ramp-up speed, but will not provide you with a scalable and resilience deployment.

To overcome this and make Kerberos Vault scale, fault-tolerant and flexible, it's recommended to setup Kerberos Vault in a Kubernetes cluster.

## Managed Kubernetes vs Self-hosted Kubernetes

Just like `docker`, you bring your Kubernetes cluster where you want `edge` or `cloud`; private or public. Depending where you will host and how (e.g. managed Kubernetes cluster vs self-hosted) you'll have less/more responsibilities and/or control. Where and how is totally up to you, and your company preferences.

This installation guide will slight modify depending on if you are self-hosting or leveraging a managed Kubernetes service by a cloud provider. Within a self-hosted installation you'll be required to install specific Kubernetes resources yourself, such as persistent volumes, storage and a load balancer.

![Kerberos Vault deployments](assets/kerberosvault-deployments.svg)

## Managed Kubernetes

To simplify the installation we will start with the most common setup, where we will install Kerberos Vault on a managed Kubernetes services.

As of now there are many cloud providers such as, but not limited too, Azure, Google Cloud, AWS, and many more. Each cloud provider has build a management service on top of Kubernetes which takes over the heavy lifting of managing a cluster yourself. It makes specific resources such as built-in loadbalancers, storage, and more availble for your needs. The cloud provider manages all the complex things for you in the back-end and implements features such as 

### Introduction

Kerberos Vault requires some initial components to be installed. If you run Kerberos Vault in the same cluster as where you have a Kerberos Factory installed, there is not much to do, and you might skip the paragraphs with prerequisite.

If you plan to run Kerberos Vault in a different cluster (which is perfectly possible), you will need to make sure you complete the initial setup of the [Kerberos Factory installation](/factory/installation). To be more specific you will need to have following components running:

- Helm
- MongoDB
- Traefik (or alternatively Nginx ingress)

We'll assume you are starting an installation from scratch and therefore install the prerequisites first.

### Clone Kerberos Vault

We'll start by cloning the configurations from our [Github repo](https://github.com/kerberos-io/vault). This repo contains all the relevant configuration files required.

    git clone https://github.com/kerberos-io/vault

### Prerequisite: Helm

Next we will install a couple of dependencies which are required for Kerberos Vault. [**Helm**](https://helm.sh/) is a package manager for Kubernetes, it helps you to set up services more easily (this could be a MQTT broker, a database, etc).
Instead of writing yaml files for every service we need, we use so-called Charts (libraries), that you can reuse and configure the, with the appropriate settings.

Use one of the preferred OS package managers to install the Helm client:

    brew install helm

    choco install kubernetes-helm

    scoop install helm

    gofish install helm

### Prerequisite: Traefik

[**Traefik**](https://containo.us/traefik/) is a reverse proxy and load balancer which allows you to expose your deployments more easily. Kerberos uses Traefik to expose its APIs more easily.

Add the Helm repository and install traefik.

    kubectl create namespace traefik
    helm repo add traefik https://helm.traefik.io/traefik
    helm install traefik traefik/traefik -n traefik 

After installation, you should have an IP attached to Traefik service, look for it by executing the `get service` command. You will see the ip address in the `EXTERNAL-IP` attribute.

    kubectl get svc

        NAME                        TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)                      AGE
        kubernetes                  ClusterIP      10.0.0.1       <none>          443/TCP                      36h
    --> traefik                     LoadBalancer   10.0.27.93     40.114.168.96   443:31623/TCP,80:31804/TCP   35h
        traefik-dashboard           NodePort       10.0.252.6     <none>          80:31146/TCP                 35h

Go to your DNS provider and link the domain you've configured in the first step `traefik.domain.com` to the IP address of thT `EXTERNAL-IP` attribute. When browsing to `traefik.domain.com`, you should see the traefik dashboard showing up.

### Prerequisite: Ingress-Nginx (alternative for Traefik)

If you don't like `Traefik` but you prefer `Ingress Nginx`, that works as well.

    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm repo update
    kubectl create namespace ingress-nginx
    helm install ingress-nginx -n ingress-nginx ingress-nginx/ingress-nginx

### Prerequisite: MongoDB

When using Kerberos Vault, it will persist references to the recordings stored in your storage provider in a MongoDB database. As used before, we are using `helm` to install MongoDB in our Kubernetes cluster.

Have a look into the `./vault/yaml/mongodb/values.yaml` file, you will find plenty of configurations for the MongoDB helm chart. To change the username and password of the MongoDB instance, go ahead and [find the attribute where](https://github.com/kerberos-io/factory/blob/master/yaml/mongodb/values.yaml#L75) you can change the root password.

    helm repo add bitnami https://charts.bitnami.com/bitnami
    kubectl create namespace mongodb
    helm install mongodb -n mongodb bitnami/mongodb --values ./vault/yaml/mongodb/values.yaml

Once installed successfully, we should verify if the password has been set correctly. Print out the password using `echo $MONGODB_ROOT_PASSWORD` and confirm the password is what you've specified in the `values.yaml` file.

    export MONGODB_ROOT_PASSWORD=$(kubectl get secret -n mongodb mongodb -o jsonpath="{.data.mongodb-root-password}" | base64 --decode)
    echo $MONGODB_ROOT_PASSWORD
