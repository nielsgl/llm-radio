from unittest.mock import MagicMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from llm_radio.api_server import app, lifespan

client = TestClient(app)


@patch("llm_radio.api_server.predictor")
def test_read_question_endpoint(mock_predictor: MagicMock) -> None:
    """
    Tests the /q/ endpoint to ensure it calls the predictor and
    returns the correct answer.
    """
    # Configure the mock to return a specific answer
    mock_predictor.return_value = MagicMock(answer="Mocked LLM answer.")

    response = client.get("/q/?q=test question")

    # Verify the predictor was called correctly
    mock_predictor.assert_called_once_with(question="test question")

    # Verify the response
    assert response.status_code == 200
    assert response.json() == {"answer": "Mocked LLM answer."}


def test_read_question_requires_query_param() -> None:
    """
    Tests that the /q/ endpoint returns a 422 Unprocessable Entity
    error if the required 'q' query parameter is missing.
    """
    response = client.get("/q/")
    assert response.status_code == 422


@pytest.mark.asyncio
@patch("dspy.configure")
@patch("dspy.LM")
@patch("os.getenv")
async def test_lifespan_success(
    mock_getenv: MagicMock, mock_lm: MagicMock, mock_configure: MagicMock
) -> None:
    """
    Tests the lifespan function for successful configuration.
    """
    mock_getenv.side_effect = [
        "test_model",
        "test_api_key",
        "test_api_base",
    ]

    async with lifespan(FastAPI()):
        pass

    mock_lm.assert_called_once_with(
        model="test_model", api_key="test_api_key", api_base="test_api_base"
    )
    mock_configure.assert_called_once()


@pytest.mark.asyncio
@patch("os.getenv", return_value=None)
async def test_lifespan_missing_env_var(mock_getenv: MagicMock) -> None:
    """
    Tests that the lifespan function raises a ValueError if an env var is missing.
    """
    with pytest.raises(ValueError, match="LLM_MODEL environment variable not set."):
        async with lifespan(FastAPI()):
            pass
