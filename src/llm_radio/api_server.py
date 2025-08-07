from fastapi import FastAPI

app = FastAPI()


@app.get("/q/")
def read_question(q: str) -> dict[str, str]:
    """
    Accepts a question and returns a hardcoded answer.
    This is the initial implementation for testing purposes.
    """
    return {"answer": "This is a hardcoded answer."}
