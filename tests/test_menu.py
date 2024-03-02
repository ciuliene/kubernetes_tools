import unittest
from unittest.mock import patch
from src.menu import Menu


class TestMenu(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        self._options = ["Add", "Subtract", "Multiply", "Divide", "Quit"]
        super().__init__(methodName)

    @patch("sys.stdout.write")
    @patch("builtins.print")
    def test_printing_menu_prints_expected_options(self, mock_print, *_):
        # Arrange
        menu = Menu(self._options)

        # Act
        menu.print_menu()

        # Assert
        for i, option in enumerate(self._options):
            actual_option = mock_print.call_args_list[i][0][0]
            self.assertIn(option, actual_option)
            color = 10
            if i == 0:
                color = 37
            self.assertIn(str(color), actual_option)

    @patch("sys.stdout.write")
    @patch("builtins.print")
    def test_printing_menu_prints_expected_options_with_left_padding(self, mock_print, *_):
        # Arrange
        menu = Menu(self._options)

        # Act
        menu.print_menu(2)

        # Assert
        for i, option in enumerate(self._options):
            actual_option = mock_print.call_args_list[i][0][0]
            self.assertIn(f'  {option}', actual_option)
            color = 10
            if i == 0:
                color = 37
            self.assertIn(str(color), actual_option)

    @patch('readchar.readkey', side_effect=['\n'])
    @patch("sys.stdout.write")
    @patch("builtins.print")
    def test_running_menu_returns_default_option(self, *_):
        # Arrange
        menu = Menu(self._options)

        # Act
        result = menu.run_menu()

        # Assert
        self.assertEqual(result, self._options[0])

    @patch('readchar.readkey', side_effect=['\x1b[B', '\x1b[B', '\n'])
    @patch("sys.stdout.write")
    @patch("builtins.print")
    def test_running_menu_returns_selected_option(self, *_):
        # Arrange
        menu = Menu(self._options)

        # Act
        result = menu.run_menu()

        # Assert
        self.assertEqual(result, self._options[2])

    @patch('readchar.readkey', side_effect=['\x1b[A', '\n'])
    @patch("sys.stdout.write")
    @patch("builtins.print")
    def test_running_menu_returns_first_option(self, *_):
        # Arrange
        menu = Menu(self._options)

        # Act
        result = menu.run_menu()

        # Assert
        self.assertEqual(result, self._options[0])

    @patch('readchar.readkey', side_effect=['a', '\n'])
    @patch("sys.stdout.write")
    @patch("builtins.print")
    def test_running_menu_returns_default_option_when_unexpected_key_is_pressed(self, *_):
        # Arrange
        menu = Menu(self._options)

        # Act
        result = menu.run_menu()

        # Assert
        self.assertEqual(result, self._options[0])

    @patch('readchar.readkey', side_effect=['\n'])
    @patch("sys.stdout.write")
    @patch("builtins.print")
    def test_running_menu_returns_default_index(self, *_):
        # Arrange
        menu = Menu(self._options)

        # Act
        result = menu.run_menu(get_index=True)

        # Assert
        self.assertEqual(result, 0)

    @patch('readchar.readkey', side_effect=['\x1b[B', '\x1b[B', '\n'])
    @patch("sys.stdout.write")
    @patch("builtins.print")
    def test_running_menu_returns_selected_index(self, *_):
        # Arrange
        menu = Menu(self._options)

        # Act
        result = menu.run_menu(get_index=True)

        # Assert
        self.assertEqual(result, 2)

    @patch('readchar.readkey', side_effect=['\x1b[A', '\n'])
    @patch("sys.stdout.write")
    @patch("builtins.print")
    def test_running_menu_returns_first_index(self, *_):
        # Arrange
        menu = Menu(self._options)

        # Act
        result = menu.run_menu(get_index=True)

        # Assert
        self.assertEqual(result, 0)

    @patch('readchar.readkey', side_effect=['a', '\n'])
    @patch("sys.stdout.write")
    @patch("builtins.print")
    def test_running_menu_returns_default_index_when_unexpected_key_is_pressed(self, *_):
        # Arrange
        menu = Menu(self._options)

        # Act
        result = menu.run_menu(get_index=True)

        # Assert
        self.assertEqual(result, 0)

    @patch('builtins.exit', side_effect=Exception)
    @patch('readchar.readkey', side_effect=['q'])
    @patch("sys.stdout.write")
    @patch("builtins.print")
    def test_quitting_menu_with_key_succeeds(self, *_):
        # Arrange
        menu = Menu(self._options)

        # Act & Assert
        self.assertRaises(Exception, menu.run_menu)

    @patch('builtins.exit', side_effect=KeyboardInterrupt)
    @patch('readchar.readkey', side_effect=['q'])
    @patch("sys.stdout.write")
    @patch("builtins.print")
    def test_quitting_menu_with_key_combination_succeeds(self, *_):
        # Arrange
        menu = Menu(self._options)

        # Act & Assert
        self.assertRaises(KeyboardInterrupt, menu.run_menu)


if __name__ == "__main__":
    unittest.main()
