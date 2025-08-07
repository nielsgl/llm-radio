# LLM Radio 📻

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/badge/packaging-uv-black.svg)](https://github.com/astral-sh/uv)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linter: ruff](https://img.shields.io/badge/linter-ruff-purple.svg)](https://github.com/astral-sh/ruff)
[![Tests](https://img.shields.io/badge/tests-pytest-green.svg)](https://pytest.org/)
[![Test Coverage](https://img.shields.io/badge/coverage-90%25+-success.svg)](#)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)
[![Gitmoji](https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg)](https://gitmoji.dev)

Serve Large Language Model (LLM) responses over the DNS protocol. This project provides a modular and extensible framework for interacting with LLMs through unconventional protocols.

## 🚀 Features

*   Query LLMs via standard DNS `TXT` record lookups.
*   Modular two-part design (DNS Server + API Server).
*   Fully type-annotated, linted, and tested codebase.
*   Extensible architecture for adding new protocols.

## 🏗️ Project Plan

This project is being built incrementally. Here is the development roadmap:

- [x] **Step 1: Project Scaffolding & Initial Documentation**
- [x] **Step 2: Implement the Core API Server**
- [x] **Step 3: Implement the Core DNS Server**
- [x] **Step 4: Integrate DNS and API Servers**
- [x] **Step 5: Add DSPy LLM Logic to API Server**
- [x] **Step 6: Finalize Error Handling and Edge Cases**

## 🛠️ Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd llm-radio
    ```

2.  **Create a virtual environment and install dependencies:**
    This project uses `uv` for package management.
    ```bash
    uv venv --clear
    uv sync --all-extras
    ```

3.  **Set up pre-commit hooks:**
    ```bash
    uv run pre-commit install
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the project root and add your LLM API key:
    ```
    LLM_API_KEY="your-secret-key-here"
    ```

## Usage

1.  **Run the API Server:**
    ```bash
    uv run uvicorn src.llm_radio.api_server:app --host 0.0.0.0 --port 8000
    ```

2.  **Run the DNS Server (in a separate terminal):**
    ```bash
    uv run python src/llm_radio/dns_server.py
    ```

3.  **Query the server:**
    ```bash
    dig @localhost -p 1053 "your question here" TXT +short
    ```

## 🧪 Development & Testing

To run the test suite and generate a coverage report:

```bash
uv run pytest --cov=src/llm_radio --cov-report=term-missing --cov-fail-under=90
