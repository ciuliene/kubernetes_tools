import subprocess
from src.custom_log import *
from src.menu import Menu
import argparse


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Kubernetes shell: a shell to interact with kubernetes clusters")

    parser.add_argument("-c", "--clusters",
                        help="current cluster", action="store_true")
    parser.add_argument("-d", "--deployments",
                        help="deployments info", action="store_true")
    parser.add_argument("-ns", "--namespaces",
                        help="namespaces", action="store_true")
    parser.add_argument("-f", "--filter",
                        help="filter criteria separated by comma to filter the pods", action="store", default=None)

    args = parser.parse_args()

    return args


KUBE = 'kubectl'

def banner():
    print("\n".join([txt_color('green') + r" _         _____   _______   _________ _______  _______  _        _______",
                     r"| \    /\ / ___ \ (  ____ \  \__   __/(  ___  )(  ___  )( \      (  ____ \ ",
                      r"|  \  / /( (___) )| (    \/     ) (   | (   ) || (   ) || (      | (    \/ ",
                      r"|  (_/ /  \     / | (_____      | |   | |   | || |   | || |      | (_____ ",
                      r"|   _ (   / ___ \ (_____  )     | |   | |   | || |   | || |      (_____  ) ",
                      r"|  ( \ \ ( (   ) )      ) |     | |   | |   | || |   | || |            ) |",
                      r"|  /  \ \( (___) )/\____) |     | |   | (___) || (___) || (____/\/\____) |",
                      r"|_/    \/ \_____/ \_______)     )_(   (_______)(_______)(_______/\_______)",
                      reset_code]))


def run_shell(cmd: list = [], capture_output: bool = True) -> str | None:
    response = subprocess.run(cmd, capture_output=capture_output, check=True).stdout

    if response is not None:
        return response.decode("utf-8")
    else:
        return None

commands = [
    {
        "id": 0, 
        "txt": "Execute the bash shell of the container",
        "cmd": lambda pod: [KUBE, "exec", pod, "--stdin", "--tty", "shell-demo", "--", "/bin/bash"],
        "args": []
    }, 
    {
        "id": 1, 
        "txt": "See the log of the container in real-time",
        "cmd": lambda pod: [KUBE, "logs", pod],
        "args": [
            {
            "text": "Tail",
            "flag": "--tail",
            "type": "int",
            "default": 10
            },
            {
            "text": "Follow",
            "flag": "-f",
            "type": "bool",
                "default": False,
                "options": ["No", "Yes"]
            }
        ]
    },
    ]


def get_clusters() -> list[dict]:
    response = run_shell(
        [KUBE, "config", "get-contexts", "-o", "name"])

    if response is not None:
        response = response.split("\n")
    else:
        response = []

    current = None

    try:
        current = get_current_cluster()
    except Exception as ex:
        log_message(f"EXCEPTION: {ex}", 'yellow')

    return [{'name': name, 'current': name == current} for name in response if len(name) > 0]


def get_current_cluster() -> str | None:
    response = run_shell([KUBE, "config", "current-context"])
    if response is not None:
        return response.strip()
    else:
        return None


def set_current_cluster() -> bool:
    try:
        clusters = get_clusters()

        options = [
            f' {"*" if x["current"]else " "} {x["name"]}' for x in clusters
        ]

        menu = Menu(options=options)

        selected_cluster_index = int(menu.run_menu(
            title="Select the cluster:", get_index=True))

        cluster_name = clusters[selected_cluster_index]['name']

        run_shell([KUBE, "config", "use-context", cluster_name])

        log_message(
            f"Current cluster: {txt_color('cyan')}{get_current_cluster()}{reset_code}\n")
    except KeyboardInterrupt:
        exit(0)
    except Exception as ex:
        log_message(f"EXCEPTION: {ex}", 'red')
        exit(-1)

    return True


def set_deployment_replicas() -> bool:
    cmd_result = run_shell([KUBE, "get", "deployments"])

    if cmd_result is None:
        log_message("No deployments found", 'yellow')
        exit(-1)

    response = cmd_result.split("\n")

    title = f"Select a deployment:\n{response[:1][0]}"
    deployments = response[1:]
    deployments = [x for x in deployments if len(x) > 0]

    if len(deployments) == 0:
        log_message("No deployments found", 'yellow')
        exit(-1)

    menu = Menu(options=deployments)

    deployment = str(menu.run_menu(title=title)).split(" ")[0]

    replicas = input("Number of replicas: ")

    try:
        replicas = int(replicas)
        if replicas < 0:
            raise ValueError("Replicas must be a non-negative integer")
    except Exception as ex:
        log_message(f"Invalid input: {ex}", 'red')
        exit(-1)

    run_shell(
        [KUBE, "scale", f"deployment/{deployment}", f"--replicas={replicas}"])

    log_message(
        f"Deployment {txt_color('cyan')}{deployment}{reset_code} has been scaled to {txt_color('cyan')}{replicas}{reset_code}\n")

    return True


def get_current_namespace() -> str:
    response = run_shell(
        [KUBE, "config", "view", "--minify", "--output", "jsonpath={..namespace}"])
    if response is not None:
        return response.strip()
    else:
        return "default"


def set_namespaces() -> bool:
    cmd_result = run_shell(
        [KUBE, "get", "namespaces"])

    if cmd_result is None:
        log_message("No namespaces found", 'yellow')
        exit(-1)

    response = cmd_result.split("\n")

    current = get_current_namespace()

    namespaces = response[1:]
    namespaces = [x for x in namespaces if len(x) > 0]

    if len(namespaces) == 0:
        log_message("No namespaces found", 'yellow')
        exit(-1)

    menu = Menu(options=[f"{'  ' if not current.lower()
                in x.lower() else '* '}{x}" for x in namespaces])

    index = int(menu.run_menu(
        title="Select a namespace:", get_index=True))

    namespace = namespaces[index].split(" ")[0]

    run_shell([KUBE, "config", "set-context",
              "--current", "--namespace", namespace])

    log_message(
        f"Current namespace: {txt_color('cyan')}{namespace}{reset_code}\n")

    return True

def main(filter: str | None = None):
    try:
        print(
            f"Current cluster: {txt_color('cyan')}{get_current_cluster()}{reset_code}\n")

        cmd = [KUBE, "get", "pods"]

        cmd_result = run_shell(cmd)

        if cmd_result is None:
            log_message("No pods found", 'yellow')
            exit(-1)

        response = cmd_result.split("\n")

        all_pods = response[1:]
        pod_list = []

        if filter is not None:
            filters = filter.split(",")
            pod_list += [
                x for x in all_pods if all([y.lower() in x.lower() for y in filters])]
        else:
            pod_list = all_pods

        if len(pod_list) == 0:
            log_message("No pods found", 'yellow')
            exit(-1)

        title = f"Select a pod:\n{response[:1][0]}"

        pod_list = [x for x in pod_list if len(x) > 0]

        menu = Menu(options=pod_list)

        pod = str(menu.run_menu(title=title)).split(" ")[0]

        menu = Menu(options=[x['txt'] for x in commands])
        id = menu.run_menu(title="Select the command:", get_index=True)

        id = int(id)

        feature = commands[id]

        cmd = feature['cmd'](pod)
        args = feature['args']

        for arg in args:
            title = f"{arg['text']} (default is {arg['default']})"
            if arg['type'] == 'int':
                val = arg['default']
                while True:
                    try:
                        f_val = input(f"{title}: ")
                        if f_val == '':
                            break
                        val = int(f_val)
                        if val < 0:
                            raise ValueError("negative")
                        break
                    except Exception as ex:
                        log_message(f"Input must be a positive integer", 'red')
                cmd.append(arg['flag'])
                cmd.append(f"{val}")
            elif arg['type'] == 'bool':
                menu = Menu(options=arg['options'])
                enable_flag = menu.run_menu(title=title, get_index=True)
                print(enable_flag)
                if enable_flag == 1:
                    cmd.append(f"{arg['flag']}")
        
        log_message("\033c", end="")

        log_message(" ".join(cmd), text_color='cyan')

        run_shell(cmd, False)
        
    except KeyboardInterrupt:  # pragma: no cover
        exit(0)

    except Exception as ex:
        log_message(f"EXCEPTION: {ex}", 'red')
        exit(-1)

    return True


if __name__ == "__main__":  # pragma: no cover
    banner()

    args = get_arguments()

    if args.clusters is True:
        set_current_cluster()
    elif args.deployments is True:
        set_deployment_replicas()
    elif args.namespaces is True:
        set_namespaces()
    else:
        main(filter=args.filter)
