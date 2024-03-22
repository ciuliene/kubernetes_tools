# Kubernetes Tools

[![Python application](https://github.com/ciuliene/kubernetes_tools/actions/workflows/python-app.yml/badge.svg?event=pull_request)](https://github.com/ciuliene/kubernetes_tools/actions/workflows/python-app.yml) [![codecov](https://codecov.io/gh/ciuliene/kubernetes_tools/graph/badge.svg?token=XH7I1SGO3M)](https://codecov.io/gh/ciuliene/kubernetes_tools)

**Kubernetes Tools** can connect to Kubernetes (K8S) and execute some commands without using the command line interface.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Description](#description)
- [Usage](#usage)
  - [Arguments](#arguments)
  - [Pods](#pods)
    - [Execute the bash shell of the container](#execute-the-bash-shell-of-the-container)
    - [Get the log of a container in real-time](#get-the-log-of-a-container-in-real-time)
  - [Clusters](#clusters)
  - [Deployments](#deployments)

## Prerequisites

This tool uses `python` (version 3.11.x or higher) and `kubectl` to connect to a K8S cluster. Both softwares must be installed and properly configured. For more information, please visit these links:

- [python](https://www.python.org/downloads/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

### Setup for cloud providers

If you want to use this tool with a cloud provider (like Azure, AWS or Google Cloud) you must have the proper CLI installed and configured.

Here is an example for Azure: To connect to an Azure Kubernetes Service (AKS) cluster, you must have the `azure-cli` installed and properly configured. To configure the K8S context, issue this command:

```sh
az aks get-credentials --resource-group <resource-group> --name <cluster-name>
```

This command must be issued for each cluster you want to manage.

## Description

This project aims to simplify operations with K8S containers. Here is the list of developed features:

| Feature | Description | Command |
| --- | --- | --- |
| Bash | Execute a bash shell in a container | `kubectl exec <pod> --stdin --tty shell-demo -- /bin/bash` |
| Log | Get the log of a container in real-time | `kubectl logs <pod>` |

Other useful features are:

- Set the current K8S context (if there are more than one):
- Set the the number of replicas of a deployment (deployment scaling)

## Usage

**NOTE**: It is recommended to use this tool inside a virtual environment.

To do this, create a virtual environment:

```sh
python -m venv <virtual-env-name> # .gitignore is already set to ignore folder called "venv"
```

and activate it (for Linux and MacOS) with this command:

```sh
source <virtual-env-name>/bin/activate
```

For more information see this [link](https://docs.python.org/3/library/venv.html)

Install required packages:

```sh
python -m pip install -r requirements.txt
```

### Arguments

| Argument | Flag | Description |
| --- | --- | --- |
| Pods |  | Run the main script to management your pods |
| Filter | `-f` or `--filter` | Run the main script getting filtered pods list |
| Clusters | `-c` or `--clusters` | List all clusters and set the active one |
| Deployments | `-d` or `--deployments` | List all deployments and set the number of replicas |

Run the script with the desired argument. For example, to list all clusters and set the active one:

```sh
python main.py --clusters # or -c
```

To list all deployments and set the number of replicas:

```sh
python main.py --deployments # or -d
```

To manage your pods:

```sh
python main.py
```

To manage filtered pod list:

```sh
python main.py -f <filters-separated-by-comma> # or --filter
```

### Pods

Once the script is started, it tries to get the list of available pods inside the selected K8S (`kubectl get pods`). Using arrow keys _up_ and _down_ for moving and _enter_ key to select, the user can choose a pod and then run one of these command:

- Execute the bash shell of the container
- See the log of the container in real-time

To stop the script use the escape sequence `CTRL+C`.

#### Execute the bash shell of the container

Using this command, the user will be able to execute the shell of a container and run shell commands within it.

#### Get the log of a container in real-time

For this action, the user will be ask for two other arguments:

| Argument | Flag   | Description                             | Type    |
| -------- | ------ | --------------------------------------- | ------- |
| Tail     | --tail | Get the tail of the log (default is 10) | Integer |
| Follow   | -f     | Follow the log (default is false)       | Bool    |

### Clusters

This command lists all clusters and set the active one. The user can choose a cluster using arrow keys _up_ and _down_ for moving and _enter_ key to select.

### Deployments

This command lists all deployments and set the number of replicas. The user can choose a deployment using arrow keys _up_ and _down_ for moving and _enter_ key to select. Then the user will be asked for the number of replicas (greater than or equal to zero).
