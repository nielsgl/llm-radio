import logging
import os
import time
from typing import Any

import coloredlogs
from dnslib import QTYPE, RR, TXT
from dnslib.server import BaseResolver, DNSServer
from dotenv import load_dotenv
import requests

coloredlogs.install(level="INFO", fmt="[%(levelname)s] %(message)s")


def chunk_answer(answer: str, max_len: int = 4096, chunk_size: int = 255) -> list[bytes]:
    """
    Chunks a string into a list of bytes, each chunk not exceeding
    chunk_size, with a total max length of max_len.
    """
    if len(answer) > max_len:
        answer = answer[: max_len - 3] + "..."

    encoded_answer = answer.encode("utf-8")
    return [encoded_answer[i : i + chunk_size] for i in range(0, len(encoded_answer), chunk_size)]


class ApiResolver(BaseResolver):
    """
    A DNS resolver that queries the API server to get the answer.
    """

    def __init__(self) -> None:
        load_dotenv()
        self.api_url = os.getenv("API_URL", "http://127.0.0.1:8000/q/")

    def resolve(self, request: Any, handler: Any) -> Any:
        """
        Resolves the DNS request by calling the API server.

        Args:
            request: The DNS request packet.
            handler: The handler for the request.

        Returns:
            The DNS response packet.
        """
        reply = request.reply()
        qname = request.q.qname
        qtype = request.q.qtype

        if qtype == QTYPE.TXT:
            question = str(qname).rstrip(".")
            pretty_question = question.replace("\\032", " ")
            logging.info(f"Received question: {pretty_question}")
            try:
                response = requests.get(self.api_url, params={"q": question}, timeout=10)
                response.raise_for_status()
                answer = response.json()["answer"]
                logging.info(f"Received answer from API: {answer[:100]}...")
                chunked_answer = chunk_answer(answer)
                reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(chunked_answer)))
            except requests.exceptions.RequestException as e:
                logging.error(f"Error calling API: {e}")
                reply.header.rcode = 2  # SERVFAIL
        else:
            reply.header.rcode = 2  # NOTIMP

        return reply


def create_server(address: str = "0.0.0.0", port: int = 1053) -> DNSServer:
    """Creates a DNSServer instance."""
    resolver = ApiResolver()
    return DNSServer(resolver, port=port, address=address)


def main() -> None:  # pragma: no cover
    """
    Starts the DNS server.
    """
    server = create_server()
    logging.info("Starting DNS server on port 1053...")
    server.start_thread()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        logging.info("Stopping DNS server.")
        server.stop()


if __name__ == "__main__":  # pragma: no cover
    main()
