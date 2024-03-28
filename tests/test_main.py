import unittest
from unittest.mock import patch
from main import *
from tests.mocks import *


@patch('builtins.print')
class TestMain(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    @patch('sys.argv', ['main.py'])
    def test_getting_arguments_returns_default_args(self, *_):
        # Act
        actual = get_arguments()

        # Assert
        self.assertFalse(actual.clusters)
        self.assertFalse(actual.deployments)
        self.assertIsNone(actual.filter)

    @patch('sys.argv', ['main.py', '-c'])
    def test_getting_arguments_returns_clusters_option(self, *_):
        # Act
        actual = get_arguments()

        # Assert
        self.assertTrue(actual.clusters)
        self.assertFalse(actual.deployments)
        self.assertIsNone(actual.filter)

    @patch('sys.argv', ['main.py', '--clusters'])
    def test_getting_arguments_returns_explicit_clusters_option(self, *_):
        # Act
        actual = get_arguments()

        # Assert
        self.assertTrue(actual.clusters)
        self.assertFalse(actual.deployments)
        self.assertIsNone(actual.filter)

    @patch('sys.argv', ['main.py', '-d'])
    def test_getting_arguments_returns_deployments_option(self, *_):
        # Act
        actual = get_arguments()

        # Assert
        self.assertFalse(actual.clusters)
        self.assertTrue(actual.deployments)
        self.assertIsNone(actual.filter)

    @patch('sys.argv', ['main.py', '--deployments'])
    def test_getting_arguments_returns_explicit_deployments_option(self, *_):
        # Act
        actual = get_arguments()

        # Assert
        self.assertFalse(actual.clusters)
        self.assertTrue(actual.deployments)
        self.assertIsNone(actual.filter)

    @patch('sys.argv', ['main.py', '-f'])
    def test_getting_arguments_raises_error_filter_has_no_option_argument(self, *_):
        # Act
        def act(): return get_arguments()

        # Assert
        self.assertRaises(SystemExit, act)

    @patch('sys.argv', ['main.py', '-f', 'filter'])
    def test_getting_arguments_returns_filter_option(self, *_):
        # Act
        actual = get_arguments()

        # Assert
        self.assertFalse(actual.clusters)
        self.assertFalse(actual.deployments)
        self.assertEqual(actual.filter, 'filter')

    def test_banner_returns_expected_string(self, mock_print, *_):
        # Arrange
        expected = "\n".join([txt_color('green') + r" _         _____   _______   _________ _______  _______  _        _______",
                             r"| \    /\ / ___ \ (  ____ \  \__   __/(  ___  )(  ___  )( \      (  ____ \ ",
                              r"|  \  / /( (___) )| (    \/     ) (   | (   ) || (   ) || (      | (    \/ ",
                              r"|  (_/ /  \     / | (_____      | |   | |   | || |   | || |      | (_____ ",
                              r"|   _ (   / ___ \ (_____  )     | |   | |   | || |   | || |      (_____  ) ",
                              r"|  ( \ \ ( (   ) )      ) |     | |   | |   | || |   | || |            ) |",
                              r"|  /  \ \( (___) )/\____) |     | |   | (___) || (___) || (____/\/\____) |",
                              r"|_/    \/ \_____/ \_______)     )_(   (_______)(_______)(_______/\_______)",
                              reset_code])

        # Act
        banner()

        # Assert
        mock_print.assert_called_once_with(expected)

    @patch('subprocess.run')
    def test_run_shell_returns_expected_string(self, mock_run, *_):
        # Arrange
        expected = "Hello, World!"
        mock_run.return_value = MockSubProcess(expected)

        # Act
        actual = run_shell(["echo", "Hello, World!"])

        # Assert
        self.assertEqual(actual, expected)

    @patch('subprocess.run')
    def test_run_shell_returns_null_when_returned_value_is_null(self, mock_run, *_):
        # Arrange
        mock_run.return_value = MockSubProcess(None)

        # Act
        actual = run_shell(["echo", "Hello, World!"])

        # Assert
        self.assertIsNone(actual)

    @patch('subprocess.run')
    def test_getting_clusters_returns_empty_list(self, mock_run, *_):
        # Arrange
        mock_run.return_value = MockSubProcess("\n")

        # Act
        actual = get_clusters()

        # Assert
        self.assertEqual(actual, [])

    @patch('main.run_shell', return_value=None)
    def test_getting_clusters_returns_empty_list_when_run_shell_returns_null(self, *_):
        # Act
        actual = get_clusters()

        # Assert
        self.assertEqual(actual, [])

    @patch('subprocess.run')
    def test_getting_clusters_returns_expected_list(self, mock_run, *_):
        # Arrange
        clusters = ["cluster-1", "cluster-2"]
        mock_run.side_effect = [MockSubProcess(
            "\n".join(clusters)), MockSubProcess("cluster-1")]

        # Act
        actual = get_clusters()

        # Assert
        for i, expected in enumerate(clusters):
            self.assertEqual(actual[i]["name"], expected)
            isCurrent = actual[i]["current"]
            if expected == 'cluster-1':
               self.assertTrue(isCurrent)
            else:
                self.assertFalse(isCurrent)

    @patch('subprocess.run')
    def test_getting_clusters_returns_expected_list_with_no_current_cluster(self, mock_run, *_):
        # Arrange
        clusters = ["cluster-1", "cluster-2"]
        mock_run.side_effect = [MockSubProcess(
            "\n".join(clusters)), Exception]

        # Act
        actual = get_clusters()

        # Assert
        for i, expected in enumerate(clusters):
            self.assertEqual(actual[i]["name"], expected)
            self.assertFalse(actual[i]["current"])

    @patch('readchar.readkey', side_effect=['\n'])
    @patch('subprocess.run')
    def test_setting_current_cluster_returns_expected_string(self, mock_run, *_):
        # Arrange
        mock_run.side_effect = [
            MockSubProcess("\n".join(["c1", "c2"])),
            MockSubProcess(None),
            MockSubProcess(None),
            MockSubProcess("c1")]

        # Act
        result = set_current_cluster()

        # Assert
        self.assertTrue(result)

    # Just to avoid the exit call
    @patch('builtins.exit', side_effect=ValueError)
    @patch('subprocess.run', side_effect=Exception)
    def test_setting_current_cluster_fails_when_exception_is_raised(self, *_):
        # Act & Assert
        with self.assertRaises(ValueError):
            set_current_cluster()

    # Just to avoid the exit call
    @patch('builtins.exit', side_effect=ValueError)
    @patch('subprocess.run', side_effect=KeyboardInterrupt)
    def test_setting_current_cluster_fails_when_keyboard_interrupt_is_raised(self, *_):
        # Act & Assert
        with self.assertRaises(ValueError):
            set_current_cluster()

    # Just to avoid the exit call
    @patch('builtins.exit', side_effect=ValueError)
    @patch('subprocess.run')
    def test_setting_replicas_quits_when_deployment_list_is_empty(self, mock_run, *_):
        # Arrange
        mock_run.return_value = MockSubProcess('\n'.join(['', '']))

        # Act & Assert
        with self.assertRaises(ValueError):
            set_deployment_replicas()

    # Just to avoid the exit call
    @patch('builtins.exit', side_effect=ValueError)
    @patch('main.run_shell', return_value=None)
    def test_setting_replicas_quits_when_run_shell_returns_none(self, *_):

        # Act & Assert
        with self.assertRaises(ValueError):
            set_deployment_replicas()

    # Just to avoid the exit call
    @patch('builtins.exit', side_effect=ValueError)
    @patch("builtins.input", return_value="-1")
    @patch('readchar.readkey')
    @patch('subprocess.run')
    def test_setting_replicas_quits_when_replicas_number_is_negative(self, mock_run, mock_readkey, *_):
        # Arrange
        mock_run.return_value = MockSubProcess('\n'.join(['d1', 'd2']))
        mock_readkey.side_effect = ['\n']

        # Act & Assert
        with self.assertRaises(ValueError):
            set_deployment_replicas()

    @patch("builtins.input", return_value="2")
    @patch('readchar.readkey')
    @patch('subprocess.run')
    def test_setting_replicas_succeeds(self, mock_run, mock_readkey, *_):
        # Arrange
        mock_run.side_effect = [
            MockSubProcess('\n'.join(['d1', 'd2'])),
            MockSubProcess(None)]
        mock_readkey.side_effect = ['\n']

        # Act & Assert
        result = set_deployment_replicas()

        self.assertTrue(result)

    @patch('subprocess.run')
    def test_getting_current_namespace_returns_default_when_response_is_null(self, mock_run, *_):
        # Arrange
        mock_run.return_value = MockSubProcess(None)

        # Act
        actual = get_current_namespace()

        # Assert
        self.assertEqual(actual, 'default')

    @patch('main.run_shell', return_value=None)
    def test_getting_current_namespace_returns_default_when_run_shell_returns_null(self, *_):
        # Act
        actual = get_current_namespace()

        # Assert
        self.assertEqual(actual, 'default')

    @patch('subprocess.run')
    def test_getting_current_namespace_returns_expected_string(self, mock_run, *_):
        # Arrange
        mock_run.return_value = MockSubProcess("namespace")

        # Act
        actual = get_current_namespace()

        # Assert
        self.assertEqual(actual, 'namespace')

    @patch('builtins.exit', side_effect=ValueError)
    @patch('subprocess.run')
    def test_main_quits_when_pod_list_is_empty(self, mock_run, *_):
        # Arrange
        mock_run.side_effect = [MockSubProcess(
            'current_cluster'), MockSubProcess(' ')]

        # Act & Assert
        with self.assertRaises(ValueError):
            main()

    @patch('builtins.exit', side_effect=ValueError)
    @patch('main.run_shell', return_value=None)
    def test_main_quits_when_run_shell_returns_null(self, *_):
        # Act & Assert
        with self.assertRaises(ValueError):
            main()

    @patch('builtins.exit', side_effect=ValueError)
    @patch('readchar.readkey', return_value='\n')
    @patch('subprocess.run')
    def test_main_succeds_to_run_container_shell(self, mock_run, *_):
        # Arrange
        mock_run.side_effect = [
            MockSubProcess('current_cluster'),
            MockSubProcess('\n'.join(['Name', 'p1', 'p2'])),
            MockSubProcess(None)]

        # Act
        result = main()

        # Assert
        self.assertTrue(result)

    @patch('builtins.exit', side_effect=ValueError)
    @patch("builtins.input", return_value='')
    @patch('readchar.readkey', side_effect=['\n', '\x1b[B', '\n', '\n', '\n'])
    @patch('subprocess.run')
    def test_main_succeds_to_get_container_logs_with_default_value(self, mock_run, *_):
        # Arrange
        mock_run.side_effect = [
            MockSubProcess('current_cluster'),
            MockSubProcess('\n'.join(['Name', 'p1', 'p2'])),
            MockSubProcess(None)]

        # Act
        result = main()

        # Assert
        self.assertTrue(result)

    @patch('builtins.exit', side_effect=ValueError)
    @patch("builtins.input", return_value='1')
    @patch('readchar.readkey', side_effect=['\n', '\x1b[B', '\n', '\n', '\n'])
    @patch('subprocess.run')
    def test_main_succeds_to_get_container_logs_with_custom_value(self, mock_run, *_):
        # Arrange
        mock_run.side_effect = [
            MockSubProcess('current_cluster'),
            MockSubProcess('\n'.join(['Name', 'p1', 'p2'])),
            MockSubProcess(None)]

        # Act
        result = main()

        # Assert
        self.assertTrue(result)

    @patch('builtins.exit', side_effect=ValueError)
    @patch("builtins.input", side_effect=['invalid', '-1', '1'])
    @patch('readchar.readkey', side_effect=['\n', '\x1b[B', '\n', '\n'])
    @patch('subprocess.run')
    def test_main_succeds_to_get_container_logs_at_third_attempt(self, mock_run, *_):
        # Arrange
        mock_run.side_effect = [
            MockSubProcess('current_cluster'),
            MockSubProcess('\n'.join(['Name', 'p1', 'p2'])), 
            MockSubProcess(None)]

        # Act
        result = main()

        # Assert
        self.assertTrue(result)

    @patch('builtins.exit', side_effect=ValueError)
    @patch("builtins.input", return_value='1')
    @patch('readchar.readkey', side_effect=['\n', '\x1b[B', '\n', '\x1b[B', '\n'])
    @patch('subprocess.run')
    def test_main_succeds_to_get_container_logs(self, mock_run, *_):
        # Arrange
        mock_run.side_effect = [
            MockSubProcess('current_cluster'),
            MockSubProcess('\n'.join(['Name', 'p1', 'p2'])), 
            MockSubProcess(None)]

        # Act
        result = main()

        # Assert
        self.assertTrue(result)

    @patch('builtins.exit')
    @patch("builtins.input", return_value='1')
    @patch('readchar.readkey', side_effect=['\n', '\x1b[B', '\n', '\x1b[B', '\n'])
    @patch('subprocess.run')
    def test_main_succeds_to_get_running_pods_logs_with_filter(self, mock_run, *_):
        # Arrange
        mock_run.side_effect = [
            MockSubProcess('current_cluster'),
            MockSubProcess("ID Name Status\n0 p1 Running"), 
            MockSubProcess(None)]

        # Act
        result = main(filter='running')

        # Assert
        self.assertTrue(result)

    @patch('builtins.exit')
    @patch("builtins.input", return_value='1')
    @patch('readchar.readkey', side_effect=['\n', '\x1b[B', '\n', '\x1b[B', '\n'])
    @patch('subprocess.run')
    def test_main_succeds_to_get_running_pods_logs_with_multiple_filters(self, mock_run, *_):
        # Arrange
        mock_run.side_effect = [
            MockSubProcess('current_cluster'),
            MockSubProcess("ID Name Status\n0 p1 Running\n1 p2 Pending\n2 p3 Error"), 
            MockSubProcess(None)]

        # Act
        result = main(filter='running,pending')


        # Assert
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
