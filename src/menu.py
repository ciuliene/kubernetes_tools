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
            txt_color = None if idx != self.selected_index else 'white'
            bg_color = None if idx != self.selected_index else "blue"
            log_message(f"{prefix}{option.ljust(longest)}",
                        text_color=txt_color, bg_color=bg_color)
            self._n_lines += 1

        for _ in range(self._n_lines):
            sys.stdout.write("\033[F")

    def __get_choice(self):
        try:
            while True:
                key = readchar.readkey()
                if key == '\x1b[A':
                    return -1
                if key == '\x1b[B':
                    return 1
                if key.lower() == 'q':
                    exit(0)
                if key == '\n':
                    return 2
                return 0
        except KeyboardInterrupt:
            exit(0)

    def run_menu(self, title: str = None, get_index: bool = False, help: bool = True) -> str | int:
        if help:
            print("Press Q key or CTRL+C combination to quit\n")
        print(title)
        while True:
            self.print_menu()
            input = self.__get_choice()

            if input == 0:
                continue

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

