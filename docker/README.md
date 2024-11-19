# Kerberos Vault in Docker

Kerberos Vault can also be installed without [a Kubernetes cluster](../kubernetes/), by leveraging plain Docker containers or `docker compose`. In this example we'll show how to setup Kerberos Vault and it's required service MongoDB. We'll use a local Minio container, but you could leverage other local storage (Ceph) or cloud storage (Minio, Storj, Google Cloud Storage, S3).

There are still some tweaks and works to do (see below), to make this setup more secure and polished.

- [ ] Implement TLS binding with Traefik
- [ ] Move to Docker volume

## :books: Overview

### Installation

1. [Prerequisites](#prerequisites)
2. [Setup networking](#setup-networking)
3. [Create host volumes](#create-host-volumes)
4. [Run the workloads](#run-the-workloads)
5. [Modify host files](#modify-host-files)

### Let's configure it!

6. [Open Minio Console](#open-minio-console)
7. [(Optional) Create Access Keys)](#optional-create-access-keys)
8. [Configure Kerberos Vault](#configure-kerberos-vault)
9. [Add a storage provider](#add-a-storage-provider)
10.  [Add an account](#add-an-account)
11.  [You're done!](#youre-done)

# Installation

We'll start with installing Kerberos Vault on your machine, VM or whatever hardware that can run the `docker` runtime. Once installed, we'll go into a quick configuration course to connect your Kerberos Vault to a storage provider.

## Prerequisites

We've created an Ubuntu 20.04 (LTS) VM on DigitalOcean, and installed `docker` and `docker-compose` using the general installation. Follow [Docker installation here.](https://docs.docker.com/engine/install/ubuntu/)

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

Now we are ready to start the `docker compose` configuration. While creating we will create several services:

- Traefik: will be used as an `Ingress` to reach our other services.
- Kerberos Vault: The application that stores recordings from Kerberos Agent in a storage provider; minio for this example.
- Minio: The local object storage we are setting up.
- MongoDB: Kerberos Vault will store some metadata in a MongoDB instance.

Download the `docker-compose.yaml` file and store it on the machine.

    wget https://raw.githubusercontent.com/kerberos-io/vault/master/docker/docker-compose.yml -O docker-compose.yaml

Create the services using the `create` command.

    docker compose create

Once created you can activate the services with the `up` command.

    docker compose up

## (Optional) Modify host files

By default ports are opened on the host system, if you enabled Ingress (Traefik) you might use DNS names. Now add some records to your `/etc/hosts` file, so you can reach the Kerberos Vault instance (and API) and Minio console, through your predefined DNS name.

    x.x.x.x kerberos-vault-api.domain.tld kerberos-vault.domain.tld minio-console.domain.tld 

or using the ports you might reach the following endpoints:

- Minio: `http://localhost:9090`
- Kerberos Vault: `http://localhost:80`

# Let's configure it!

Now the services are up and running, you should be able to access both the Kerberos Vault application and the Minio console. You can access both applications using the credentials specified in the `environment` variables.

## Open Minio Console

Open your favourite browser, and open the Minio Console - `http://localhost:9090` or if Traefik enabled: `http://minio-console.domain.tld `. You should see the Minio console showing up; depending on your version this might look different.

![Minio console](assets/minio-console.png)

Use the credentials you've defined for the Minio service. By default this is `ROOTNAME` and `CHANGEME123`. Please change that for your own configuration. Once signed in successfully, move over to the `Buckets` page by selecting the navigation item.

Once opened, select the `Create Bucket +` button to create a new bucket, propose a name of your preference. 

![Minio create bucket](assets/minio-create-bucket.png)

### (Optional) Create Access Keys

By default you'll be able to use your Minio username and password; as you used to sign into the console. However it's a better practice to create some Access keys (and secret key). Open the `Access Keys` page by selecting the navigation item, once opened press the `Create access key+` button. 

Some proposal keys are shown, modify or use as-is, copy them for your availability.

## Configure Kerberos Vault

Open a new tab in your browser and paste in the Kerberos Vault url `http://kerberos-vault.domain.tld`. The login page will show up, use the credentials you've defined for Kerberos Vault, by default this is `root` and `pass`; please modify this to your needs.

![Kerberos Vault login](assets/kerberosvault-login.png)

### Add a storage provider

To store your data, Kerberos Vault, leverages other storage solutions such as (MinIO, Storj, S3, Google Cloud Storage, Ceph, etc) to store your data. In that sense Kerberos Vault acts as a proxy between your Kerberos Agents and the persistence layer. By doing that, Kerberos Vault decouples persistence from your Kerberos Agents, and allows you to switch persistence on-the-fly. Next to this there are many more advantages such as caching, forwarding, etc.

Open the `Storage Providers` page, by selecting the navigation item. Select the `+ Add Storage Provider` button, to create a new storage provider.

![Kerberos Vault provider](assets/kerberosvault-addprovider.png)

Select the option `Minio` from the dropdown and fill-in the required fields.

- Provider name: a unique name that matches your needs.
- Bucket name: the name of the bucket you created in Minio.
- Region: not required, use `na`; stands for notapplicable.
- Hostname: this should match the minio service name, for this configuration it would be `minio:9000`, as we run minio on port `9000`.
- Access key and Secret key: the keys you have created in the optional step, or the username and password you've provided to access the console.
- SSL enabled: keep this disabled, as we didn't implement it.

Press the `validate` button, you should see a green confirmation box at the top. If not you should verify in the logs what might be going wrong.

### Add an account

Now that we have created a storage provider, we'll need to provide access to that provider by creating an account. An account contains credentials that can be used by a Kerberos Agents in the storage provider. In other words, an account protects a storage provider from external access and only allows operations on it by using the correct account credentials.

Open the account page, by selectig the `Accounts` navigation item. Select the `+ Add Account` button. Fill-in the required fields to create an account.

![Kerberos Vault account](assets/kerberosvault-addaccount.png)

- Account name: an unique name that matches your needs.
- Main provider: select the provider we have created.
- Day limit: the life time of a recording; number of days it will be persisted.
- Integrations: a message broker that will be triggered on receival of a recording.
- Directory: set it to `*`, this wildcard option allow you to leverage it for multiple users or sub directories.
- Access Key and Secret Key: Press the `Generate` button, to get some strong keys.
- Cloud analysis: Disabled, not necessary if you do not connect to Kerberos Hub.
- Edge analysis: Disabled, not required.

## You're done!

Now you are ready setting up Kerberos Vault with Minio! It's time to connect some Kerberos Agents! Let's have a look here how to do that. If you didn't already create a Kerberos Agent, [please have a look here](https://github.com/kerberos-io/agent/tree/master/deployments/docker) to understand how it's done.

### Connect Kerberos Agent to Kerberos Vault

Once you have spun up one or more agents through `docker`, `docker compose`, `Kerberos Factory` or any other automation tool you can configure your Kerberos Agents to connect to Kerberos Vault.

As you might have noticed, each Kerberos Agent will connect to a single camera, with its own dedicated agent configuration for that specific camera. This design principle allows us to support a distributed and resilent approach where workloads can be spread towards a cluster of machines.

A Kerberos Agent can be configured using various methods: `the UI`, `environment variables`, or `configuration files`. 

#### UI

When running the Kerberos Agent through one of the deployments as mentioned above you should be able reach the Kerberos Agent UI through the defined port. You should see a login screen where you can sign in with the default username and password: `root`, `root`.

![Login Kerberos agent](./assets/kerberos-agent-overview.gif)

Once signed in you should head over to the `settings` or `configuration page` and look for the `persistence` tab. Change the dropdown to `Kerberos Vault`, you will see that several details are required to be filled in, by adding the correct values we are able to set up a secure connection to `Kerberos Vault`

![Change persistence settings](./assets/kerberos-agent-to-kerberos-vault.gif)

The information we need to provide are the following fields:

- `Kerberos Vault API URL`:  The API url is hosted on the `http://{your-vault-domain}/api`, where the `/api` suffix is added to the domain of your Kerberos Vault. You can verify this by browsing to `http://{your-vault-domain}/api/health`.
- `Provider`: The storage provider you would like to use. You can find the providers on the "Storage providers" page (or specified in the Kerberos Vault account you have setup).
- `Directory`:  This is the (sub) directory where the recordings will be stored in the storage provider. Important to note is that if you want to view your recordings through Kerberos Hub, this directory has to match the username of your Kerberos Hub account.
- `Access Key`: The access key of the account you have created in previous steps.
- `Secret Key`: The secret key of the account you have created in previous steps.

Once you have filled in the relevant credentials you can hit the `Verify Connection` button and you should see a green success bar shown on top of the UI. You could also verify on your storage provider by connecting to the configured storage provider and see if a `test-provider` directory was created with a sample video.

![Verify settings](./assets/save-kerberos-vault-setings.gif)

Congratulations! Your Kerberos Agent is now successfully connected to the Kerberos Vault. You can centralize your recordings on the storage provider of your choice, whether it's Edge or Cloud. This will allow you to manage and access your recordings more efficiently and securely.
