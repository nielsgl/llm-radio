import time
from typing import Any

from dnslib import QTYPE, RR, TXT
from dnslib.server import BaseResolver, DNSServer


class HardcodedResolver(BaseResolver):
    """
    A DNS resolver that returns a hardcoded TXT record for any TXT query.
    """

    def resolve(self, request: Any, handler: Any) -> Any:
        """
        Resolves the DNS request.

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
            reply.add_answer(
                RR(
                    qname,
                    QTYPE.TXT,
                    rdata=TXT("This is a hardcoded DNS answer."),
                )
            )
        else:
            reply.header.rcode = 2  # NOTIMP

        return reply


def create_server(address: str = "0.0.0.0", port: int = 1053) -> DNSServer:
    """Creates a DNSServer instance."""
    resolver = HardcodedResolver()
    return DNSServer(resolver, port=port, address=address)


def main() -> None:  # pragma: no cover
    """
    Starts the DNS server.
    """
    server = create_server()
    print("Starting DNS server on port 1053...")
    server.start_thread()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Stopping DNS server.")
        server.stop()


if __name__ == "__main__":  # pragma: no cover
    main()
