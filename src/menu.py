import os
import readchar
from src.custom_log import log_message

class Menu():
    def __init__(self, options:list) -> None:
        self.selected_index = 0
        self.options = options
        pass
    
    def clear(self): 
        print("\033c")
    
    def print_menu(self, title:str = None):
        self.clear()
        if title is not None:
            print(title)
        for idx, option in enumerate(self.options):
            txt_color =  None if idx != self.selected_index else 'black'
            bg_color =  None if idx != self.selected_index else "white"
            log_message(option,text_color=txt_color, bg_color=bg_color)

    def get_choice(self):
        while True:
            key = readchar.readkey()
            if key == '\x1b[A':
                return -1
            if key == '\x1b[B':
                return 1
            if key == '\n':
                return 2
            try:
                choice = int(key) - 1
                if 0 <= choice < len(self.options):
                    return choice
            except ValueError:
                pass

    def run_menu(self, title: str = None, get_index:bool=False) -> str | int:
        while True:
            self.print_menu(title=title)
            input = self.get_choice()

            if input == 2:
                break
            self.selected_index += input
            self.selected_index = max(0, min(self.selected_index, len(self.options) - 1))

        if get_index == True:
            return self.selected_index

        return self.options[self.selected_index]
