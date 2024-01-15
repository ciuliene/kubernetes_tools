import readchar
from src.custom_log import *
import sys


class Menu():
    def __init__(self, options:list) -> None:
        self.selected_index = 0
        self.options = options
        self._n_lines = None
        pass

    def print_menu(self, pad=0):
        longest = 0
        for option in self.options:
            if len(option) > longest:
                longest = len(option)

        longest += pad

        prefix = ""

        for _ in range(pad):
            prefix += " "

        self._n_lines = 0
        for idx, option in enumerate(self.options):
            txt_color =  None if idx != self.selected_index else 'white'
            bg_color =  None if idx != self.selected_index else "blue"
            log_message(f"{prefix}{option.ljust(longest)}",text_color=txt_color, bg_color=bg_color)
            self._n_lines+=1

        for _ in range(self._n_lines):
            sys.stdout.write("\033[F")

    def get_choice(self):
        while True:
            key = readchar.readkey()
            if key == '\x1b[A':
                return -1
            if key == '\x1b[B':
                return 1
            if key.lower() == 'q':
                log_message("\n[END]\n", text_color='black', bg_color='yellow')
                exit(0)
            if key == '\n':
                return 2
            try:
                choice = int(key) - 1
                if 0 <= choice < len(self.options):
                    return choice
            except ValueError:
                pass

    def run_menu(self, title: str = None, get_index:bool=False) -> str | int:
        print(title)
        while True:
            self.print_menu()
            input = self.get_choice()

            if input == 2:
                break
            self.selected_index += input
            self.selected_index = max(0, min(self.selected_index, len(self.options) - 1))

        for _ in range(self._n_lines):
            sys.stdout.write("\n")

        sys.stdout.write("\n")

        if get_index == True:
            return self.selected_index

        return self.options[self.selected_index]

