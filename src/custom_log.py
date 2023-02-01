def log_message(message:str, text_color:str = None, bg_color:str = None, end: str = None):
    text_color_code = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[10m'
    }
    bg_color_code = {
        'black': '\033[40m',
        'red': '\033[41m',
        'green': '\033[42m',
        'yellow': '\033[43m',
        'blue': '\033[44m',
        'magenta': '\033[45m',
        'cyan': '\033[46m',
        'white': '\033[47m',
        'reset': '\033[10m'
    }
    reset_code = '\033[0m'
    if text_color not in text_color_code:
        text_color = 'reset'
    if bg_color not in bg_color_code:
        bg_color = 'reset'
    print(f"{bg_color_code[bg_color]}{text_color_code[text_color]}{message}{reset_code}", end='\n' if end is None else end)

if __name__ == "__main__":
    color_list = ['black',
        'red',
        'green',
        'yellow',
        'blue',
        'magenta',
        'cyan',
        'white',
        'reset']

    bg_list = [x for x in color_list]
    fg_list = [x for x in color_list]

    pad = 0

    for x in color_list:
        if pad < len(x):
            pad = len(x)
    
    pad += 2

    for fg in fg_list:
        i = 0
        for bg in bg_list:
            log_message(f"BG: {bg.ljust(pad)}\tFG: {fg.ljust(pad)}", text_color=fg, bg_color=bg)
        i+=1