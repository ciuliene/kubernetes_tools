def log_message(message:str, text_color:str = None, bg_color:str = None):
    text_color_code = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m'
    }
    bg_color_code = {
        'black': '\033[40m',
        'red': '\033[41m',
        'green': '\033[42m',
        'yellow': '\033[43m',
        'blue': '\033[44m',
        'magenta': '\033[45m',
        'cyan': '\033[46m',
        'white': '\033[47m'
    }
    reset_code = '\033[0m'
    if text_color not in text_color_code:
        text_color = 'black'
    if bg_color not in bg_color_code:
        bg_color = 'white'
    print(f"{bg_color_code[bg_color]}{text_color_code[text_color]}{message}{reset_code}")
