# Kerberos Vault in Docker

Kerberos Vault can also be installed without a Kubernetes cluster, by leveraging plain Docker containers or `docker compose`. In this example we'll show how to setup Kerberos Vault and it's required service MongoDB.

- [ ] Implement TLS binding with Traefik
- [ ] Move to Docker volume

## In this example we'll be using a clean VM

We've created an Ubuntu 20.04 (LTS) VM on DigitalOcean, and installed `docker` and `docker-compose` using the general installation.

[Follow Docker installation here](https://docs.docker.com/engine/install/ubuntu/)

## Setup networking

For this tutorial we will setup a new virtual network, which we'll name `cluster-net`.

    docker network create cluster-net

Verify if the network is successfully created.

    docker network ls

Make sure you'll locate the `cluster-net` network.

       NETWORK ID     NAME          DRIVER    SCOPE
       cf5e5c5ed641   bridge        bridge    local
    -> 75007810f24b   cluster-net   bridge    local
       4391b62e250d   host          host      local
       d5a219a216f5   none          null      local

## Create host volumes

To persist our date outside our containers, we'll make a few directories on our host machine, that we will bind to our containers.

    mkdir vault
    mkdir mongodb

## Run the workloads

Now we are ready to ...

    docker compose up

## Modify host files

Now add some records to your `/etc/hosts` file, so you can reach the Kerberos Vault instance (and API) through your predefined DNS name.

    178.xxx.xxx.41 kerberos-vault-api.domain.tld kerberos-vault.domain.tld
