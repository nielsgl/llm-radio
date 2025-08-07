from contextlib import asynccontextmanager
import os

from dotenv import load_dotenv
import dspy
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load environment variables from .env file
    load_dotenv()

    # Configure the language model
    model_name = os.getenv("LLM_MODEL")
    api_key = os.getenv("LLM_API_KEY")
    api_base = os.getenv("LLM_API_BASE")

    if not model_name:
        raise ValueError("LLM_MODEL environment variable not set.")
    if not api_key:
        raise ValueError("LLM_API_KEY environment variable not set.")

    model = dspy.LM(
        model=model_name,
        api_key=api_key,
        api_base=api_base,
    )
    dspy.configure(lm=model)
    yield


app = FastAPI(lifespan=lifespan)


class DNSQuery(dspy.Signature):
    """Answers a question asked over DNS."""

    question = dspy.InputField()
    answer = dspy.OutputField()


# Create a predictor
predictor = dspy.Predict(DNSQuery)


@app.get("/q/")
def read_question(q: str) -> dict[str, str]:
    """
    Accepts a question and returns an answer from the LLM.
    """
    result = predictor(question=q)
    return {"answer": result.answer}
