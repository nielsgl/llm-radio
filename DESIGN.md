# LLM Radio Design Document

This document outlines the architecture and design principles for the LLM Radio project.

## 1. High-Level Architecture

The system is designed with a decoupled, modular architecture consisting of two primary components:

1.  **DNS Server (`dns_server.py`)**: A lightweight, specialized server responsible for handling the DNS protocol. Its sole purpose is to receive `TXT` queries and forward the question part to the API Server.
2.  **API Server (`api_server.py`)**: A `FastAPI` application that contains all the core logic for interacting with the Large Language Model (LLM). It exposes a simple API endpoint that the DNS server (and potentially other services in the future) can call.

This decoupled design ensures that the protocol-specific handling is separate from the core application logic, making the system easier to maintain, test, and extend.

## 2. Data Flow

The data flow for a standard user query is as follows:

1.  A user issues a `dig` command to the DNS server (e.g., `dig @localhost -p 1053 "what is the capital of france" TXT +short`).
2.  The **DNS Server** receives the query, validates that it is for a `TXT` record, and extracts the question string.
3.  The DNS Server makes an HTTP GET request to the **API Server's** `/q/` endpoint, passing the question.
4.  The **API Server** receives the request and uses the `dspy-ai` library to pass the question to the configured LLM.
5.  The LLM processes the question and returns an answer.
6.  The API Server returns the answer as a plain text response to the DNS Server.
7.  The DNS Server packages the answer into a DNS `TXT` record and sends it back to the user's `dig` client.
8.  The user sees the LLM's answer directly in their terminal.

## 3. Future Work

The modular design opens up several possibilities for future expansion:

*   **Containerization**: Package the application with a `Dockerfile` for easy, reproducible deployments.
*   **Additional Protocols**: Add other interfaces to the LLM, such as:
    *   A `curl`-able HTTP endpoint.
    *   An `ssh`-based interface.
    *   A Slack bot.
*   **Response Chunking**: Implement a mechanism to handle LLM responses that exceed the DNS packet size limit, potentially by splitting the response across multiple `TXT` records.
