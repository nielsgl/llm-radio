import subprocess
from unittest.mock import MagicMock, patch

from llm_radio.client import run_dig


@patch("subprocess.run")
def test_run_dig_success(mock_run):
    """
    Tests that the run_dig function correctly calls the dig command
    and returns its output.
    """
    mock_process = MagicMock()
    mock_process.stdout = '"Mocked dig output"'
    mock_run.return_value = mock_process

    result = run_dig("test question", [], "localhost", 1053)

    mock_run.assert_called_once_with(
        ["dig", "@localhost", "-p", "1053", "test question", "TXT", "+short"],
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    )
    assert result == "Mocked dig output"


def test_run_dig_no_server_details():
    """
    Tests that an error is returned if server details are missing.
    """
    result = run_dig("test", [], "", 0)
    assert "Error: Server Address and Port must be provided." in result


@patch("subprocess.run", side_effect=FileNotFoundError)
def test_run_dig_not_found(mock_run):
    """
    Tests the error handling when the 'dig' command is not found.
    """
    result = run_dig("test", [], "localhost", 1053)
    assert "Error: 'dig' command not found" in result


@patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "dig", stderr="failure"))
def test_run_dig_called_process_error(mock_run):
    """
    Tests the error handling for a failed dig command.
    """
    result = run_dig("test", [], "localhost", 1053)
    assert "Error executing dig command:\nfailure" in result


@patch("subprocess.run", side_effect=subprocess.TimeoutExpired("dig", 10))
def test_run_dig_timeout(mock_run):
    """
    Tests the error handling for a timed out dig command.
    """
    result = run_dig("test", [], "localhost", 1053)
    assert "Error: dig command timed out." in result
