from dnslib import DNSRecord
from dnslib.server import DNSServer

from llm_radio.dns_server import HardcodedResolver, create_server


def test_resolve_txt_query() -> None:
    """
    Tests that the HardcodedResolver returns the correct
    hardcoded response for a TXT query.
    """
    resolver = HardcodedResolver()
    request = DNSRecord.question("test.com", qtype="TXT")

    response = resolver.resolve(request, handler=None)  # type: ignore

    assert len(response.rr) == 1
    assert response.rr[0].rdata.toZone() == '"This is a hardcoded DNS answer."'


def test_resolve_non_txt_query() -> None:
    """
    Tests that the HardcodedResolver returns a NOTIMP (Not Implemented)
    error for any query type other than TXT.
    """
    resolver = HardcodedResolver()
    request = DNSRecord.question("test.com", qtype="A")

    response = resolver.resolve(request, handler=None)  # type: ignore

    assert len(response.rr) == 0
    assert response.header.rcode == 2  # RCODE 2 is NOTIMP


def test_create_server() -> None:
    """
    Tests that the create_server function returns a valid DNSServer instance.
    """
    server = create_server(address="127.0.0.1", port=5353)
    assert isinstance(server, DNSServer)
    assert server.server.server_address == ("127.0.0.1", 5353)
