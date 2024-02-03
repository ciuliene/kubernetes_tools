# Kubernetes Tools

**Kubernetes Tools** can connect to Kubernetes (K8S) and execute some commands without using the command line interface.

## Prerequisites

This tool uses _kubectl_ commands. `kubectl` software must be installed and properly configured. To do so, please visit this [link](https://kubernetes.io/docs/tasks/tools/).

## Description

This project aims to simplify operations with K8S containers. Here is the list of developed features:

| Feature | Description                             | Command                                                    |
| ------- | --------------------------------------- | ---------------------------------------------------------- |
| Bash    | Execute a bash shell in a container     | `kubectl exec <pod> --stdin --tty shell-demo -- /bin/bash` |
| Log     | Get the log of a container in real-time | `kubectl logs <pod>`                                       |

Other useful features are:

- Set the current K8S context (if there are more than one):
- Set the the number of replicas of a deployment (deployment scaling)

## Usage

**NOTE**: It is recommended to use this tool inside a virtual environment. For more information see this [link](https://docs.python.org/3/library/venv.html)

Install required packages:

```sh
python -m pip install -r requirements.txt
```

### Arguments

| Argument    | Flag                    | Description                                         |
| ----------- | ----------------------- | --------------------------------------------------- |
| Pods        |                         | Run the main script to management your pods         |
| Clusters    | `-c` or `--clusters`    | List all clusters and set the active one            |
| Deployments | `-d` or `--deployments` | List all deployments and set the number of replicas |

Run the script with the desired argument. For example, to list all clusters and set the active one:

```sh
python main.py --clusters
```

To list all deployments and set the number of replicas:

```sh
python main.py --deployments
```

To manage your pods:

```sh
python main.py
```

### Pods

Once the script is started, it tries to get the list of available pods inside the selected K8S (`kubectl get pods`). Using arrow keys _up_ and _down_ for moving and _enter_ key to select, the user can choose a pod and then run one of these command:

- Execute the bash shell of the container
- See the log of the container in real-time

To stop the script use the escape sequence `CTRL+C`.

### Execute the bash shell of the container

Using this command, the user will be able to execute the shell of a container and run shell commands within it

### Get the log of a container in real-time

For this action, the user will be ask for two other arguments:

| Argument | Flag   | Description                             | Type    |
| -------- | ------ | --------------------------------------- | ------- |
| Tail     | --tail | Get the tail of the log (default is 10) | Integer |
| Follow   | -f     | Follow the log (default is false)       | Bool    |
