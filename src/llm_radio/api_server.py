from contextlib import asynccontextmanager
import logging
import os

import coloredlogs
from dotenv import load_dotenv
import dspy
from fastapi import FastAPI

coloredlogs.install(level="INFO", fmt="[%(levelname)s] %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load environment variables from .env file
    load_dotenv()

    # Suppress verbose logs from the litellm library
    logging.getLogger("litellm").setLevel(logging.WARNING)

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
    pretty_question = q.replace("\\032", " ")
    logging.info(f"Received question: {pretty_question}")
    result = predictor(question=pretty_question)
    logging.info(f"Sending answer: {result.answer[:100]}...")
    return {"answer": result.answer}
