from fastapi.testclient import TestClient

from llm_radio.api_server import app

client = TestClient(app)


def test_read_question_endpoint() -> None:
    """
    Tests the /q/ endpoint to ensure it returns the hardcoded answer.
    """
    response = client.get("/q/?q=test")
    assert response.status_code == 200
    assert response.json() == {"answer": "This is a hardcoded answer."}


def test_read_question_requires_query_param() -> None:
    """
    Tests that the /q/ endpoint returns a 422 Unprocessable Entity
    error if the required 'q' query parameter is missing.
    """
    response = client.get("/q/")
    assert response.status_code == 422
