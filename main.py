import subprocess
from src.custom_log import *
from src.menu import Menu

KUBE = 'kubectl'

def banner():
    return "\n".join([txt_color('green') + r" _         _____   _______   _________ _______  _______  _        _______",
                     r"| \    /\ / ___ \ (  ____ \  \__   __/(  ___  )(  ___  )( \      (  ____ \ ",
                      r"|  \  / /( (___) )| (    \/     ) (   | (   ) || (   ) || (      | (    \/ ",
                      r"|  (_/ /  \     / | (_____      | |   | |   | || |   | || |      | (_____ ",
                      r"|   _ (   / ___ \ (_____  )     | |   | |   | || |   | || |      (_____  ) ",
                      r"|  ( \ \ ( (   ) )      ) |     | |   | |   | || |   | || |            ) |",
                      r"|  /  \ \( (___) )/\____) |     | |   | (___) || (___) || (____/\/\____) |",
                      r"|_/    \/ \_____/ \_______)     )_(   (_______)(_______)(_______/\_______)",
                      f"{reset_code}Press Q key or CTRL+C combination to quit\n"])


def run_shell(cmd: list = [], capture_output: bool = True) -> str:
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
            "default": False
            }
        ]
    },
    ]

def main():
    try:
        print(banner())
        response = run_shell([KUBE, "get", "pods"]).split("\n")
        title = f"Select a pod:\n{response[:1][0]}"
        pod_list = response[1:]
        pod_list = [x for x in pod_list if len(x) > 0]

        menu = Menu(options=pod_list)

        pod = menu.run_menu(title=title).split(" ")[0]

        menu = Menu(options=[x['txt'] for x in commands])
        id = menu.run_menu(title="Select the command:", get_index=True)

        id = int(id)

        item = [x for x in commands if x['id'] == id]

        if len(item) != 1:
            log_message(f"Invalid selection", 'red')
            exit(-2)
        item = item[0]
        cmd = item['cmd'](pod)
        args = item['args']

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
                        break
                    except Exception as ex:
                        log_message(f"Input must be an integer", 'red')
                cmd.append(arg['flag'])
                cmd.append(f"{val}")
            elif arg['type'] == 'bool':
                menu = Menu(options=["No", "Yes"])
                enable_flag = menu.run_menu(title=title, get_index=True)
                if enable_flag == 1:
                    cmd.append(f"{arg['flag']}")
        
        log_message("\033c", end="")

        log_message(" ".join(cmd), text_color='cyan')

        run_shell(cmd, False)
        
    except KeyboardInterrupt:
        exit(0)

    except Exception as ex:
        log_message(f"EXCEPTION: {ex}", 'red')
        exit(-1)

if __name__ == "__main__":
    main()