# Kubernetes Tools

**Kubernetes Tools** can connect to Kubernetes (K8S) and execute some commands without using the command line interface.

## Prerequisites

This tool uses _kubectl_ commands. `kubectl` software must be installed and properly configured. To do so, please visit this [link](https://kubernetes.io/docs/tasks/tools/)

## Description

This project aims to simplify operations with K8S containers. Here is the list of developed features:

| Feature | Description                             | Command                                                    |
| ------- | --------------------------------------- | ---------------------------------------------------------- |
| Bash    | Execute a bash shell in a container     | `kubectl exec <pod> --stdin --tty shell-demo -- /bin/bash` |
| Log     | Get the log of a container in real-time | `kubectl attach <pod>`                                     |

## Usage

**NOTE**: It is recommended to use this tool inside a virtual environment. For more information see this [link](https://docs.python.org/3/library/venv.html)

Install required packages:

```sh
python -m pip install -r requirements.txt
```

And then run the script:

```sh
python main.py
```

Once the script is started, it tries to get the list of available pods inside the selected K8S (`kubectl get pods`). Using arrow keys _up_ and _down_ for moving and _enter_ key to select, the user can choose a pod and then run one of these command:

- Execute the bash shell of the container
- See the log of the container in real-time

To stop the script use the escape sequence `CTRL+C`.
