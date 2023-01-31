import subprocess
from src.custom_log import log_message
from src.menu import Menu

KUBE = 'kubectl'

def run_shell(cmd: list = [], capture_output: bool = True) -> str:
    response = subprocess.run(cmd, capture_output=capture_output, check=True).stdout
    
    if response is not None:
        return response.decode("utf-8")
    else:
        return None

choices = ["1", "2"]

def main():

    try:
        pod_list = run_shell([KUBE, "get", "pods"]).split("\n")[1:]
        pod_list = [x.split(" ")[0] for x in pod_list]
        pod_list = [x for x in pod_list if len(x) > 0]

        menu = Menu(options=pod_list)

        pod = menu.run_menu(title="Select the pod:")

        menu = Menu(options = ["Execute the bash shell of the container", "See the log of the container in real-time"])
        func = menu.run_menu(title="Select the command:", get_index=True)
            

        if func == 0:
            run_shell([KUBE, "exec", pod, "--stdin", "--tty", "shell-demo", "--", "/bin/bash"], False)
        elif func == 1:
            run_shell([KUBE, "attach", pod], False)
        
    except KeyboardInterrupt:
        exit()

    except Exception as ex:
        log_message(f"EXCEPTION: {ex}", 'red')
    return

if __name__ == "__main__":
    main()