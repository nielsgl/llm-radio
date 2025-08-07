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

## 🏛️ Architecture

The system consists of two core servers and a Gradio-based client. The servers can be run locally for development or deployed to a public server.

![Architecture Diagram](https://mermaid.ink/img/Z3JhcGggVEQKICAgIHN1YmdyYXBoICJVc2VyJ3MgTWFjaGluZSIKICAgICAgICBzdWJncmFwaCAidXYgdG9vbCBydW4tc2VydmVycyIKICAgICAgICAgICAgQVtBUEkgU2VydmVyIEZhc3RBUEldCiAgICAgICAgICAgIEJbRE5TIFNlcnZlciBkbnNsaWJdCiAgICAgICAgZW5kCgogICAgICAgIHN1YmdyYXBoICJ1diB0b29sIGNoYXQiCiAgICAgICAgICAgIENbR3JhZGlvIFVJXSAtLSAiZXhlY3V0ZXMiIC0tPiBEW2RpZyBjb21tYW5kXQogICAgICAgIGVuZAogICAgZW5kCgogICAgRCAtLSAicXVlcmllcyIgLS0+IEIKICAgIEIgLS0gIkhUVFAgR0VUIiAtLT4gQQoKICAgIHN1YmdyYXBoICJJbnRlcm5ldCIKICAgICAgICBFClB1YmxpYyBVc2VyXSAtLSAiZGlnIEBkbmsubWRvbWFpbi5jb20iIC0tPiBCCiAgICBlbmQKCiAgICBzdHlsZSBBIGZpbGw6I2Y5ZixzdHJva2U6IzMzMyxzdHJva2Utd2lkdGg6MnB4CiAgICBzdHlsZSBFIGZpbGw6I2NjZixzdHJva2U6IzMzMyxzdHJva2Utd2lkdGg6MnB4CiAgICBzdHlsZSBDIHN0eWxlIGZpbGw6IzlmOSxzdHJva2U6IzMzMyxzdHJva2Utd2lkdGg6MnB4)

<details>
<summary>Mermaid Diagram Source</summary>

```mermaid
graph TD
    subgraph "User's Machine"
        subgraph "uv tool run-servers"
            A[API Server FastAPI]
            B[DNS Server dnslib]
        end

        subgraph "uv tool chat"
            C[Gradio UI] -- "executes" --> D[dig command]
        end
    end

    D -- "queries" --> B
    B -- "HTTP GET" --> A

    subgraph "Internet"
        E[Public User] -- "dig @dns.domain.com" --> B
    end

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#ccf,stroke:#333,stroke-width:2px
    style C fill:#9f9,stroke:#333,stroke-width:2px
```

</details>

## 🏗️ Project Plan

This project is being built incrementally. Here is the development roadmap:

- [x] **Phase 1: Core Functionality**
- [ ] **Phase 2: Usability & Features**
  - [ ] **Step 7: Enhance Servers for Public & Unified Startup**
  - [ ] **Step 8: Implement Gradio Chat Client**
  - [ ] **Step 9: Configure `uv` tool for Gradio client**
  - [ ] **Step 10: Finalize and Document New Features**

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
    ```bash
    LLM_MODEL="your-model"
    LLM_API_KEY="your-secret-key-here"
    LLM_API_BASE="your-model-base-url"
    ```

## Usage

1.  **Run the Servers:**
    Use the `run-servers` tool to start both the API and DNS servers concurrently.
    ```bash
    uv run run-servers
    ```

2.  **Query via the Chat Interface:**
    Launch the Gradio client with the `chat` tool.
    ```bash
    uv run chat
    ```

3.  **Query via the Command Line:**
    ```bash
    dig @localhost -p 1053 "your question here" TXT +short
    ```

## 🧪 Development & Testing

To run the test suite and generate a coverage report:

```bash
uv run pytest --cov=src/llm_radio --cov-report=term-missing --cov-fail-under=90
```
