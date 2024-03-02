import unittest
from unittest.mock import patch
from src.custom_log import log_message


class TestCustomLog(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    @patch("builtins.print")
    def test_logging_message_print_expected_string(self, mock_print, *_):
        # Arrange
        message = "Hello World"

        # Act
        log_message(message)

        # Assert
        mock_print.assert_called_with(
            f'\x1b[10m\x1b[10m{message}\x1b[0m', end='\n')

    @patch("builtins.print")
    def test_logging_message_print_expected_string_with_custom_colors(self, mock_print, *_):
        # Arrange
        message = "Hello World"

        # Act
        log_message(message, 'red', 'green', '')

        # Assert
        mock_print.assert_called_with(
            f'\x1b[42m\x1b[31mHello World\x1b[0m', end='')


if __name__ == "__main__":
    unittest.main()
