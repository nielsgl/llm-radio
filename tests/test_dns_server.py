from dnslib import DNSRecord
from dnslib.server import DNSServer
import requests
from requests_mock import Mocker

from llm_radio.dns_server import ApiResolver, create_server


def test_resolve_txt_query_success(requests_mock: Mocker) -> None:
    """
    Tests that the ApiResolver returns the correct response from the API.
    """
    api_url = "http://test.com/q/"
    requests_mock.get(api_url, json={"answer": "Mocked API answer."})

    resolver = ApiResolver(api_url=api_url)
    request = DNSRecord.question("test question", qtype="TXT")

    response = resolver.resolve(request, handler=None)  # type: ignore

    assert len(response.rr) == 1
    assert response.rr[0].rdata.toZone() == '"Mocked API answer."'


def test_resolve_txt_query_api_error(requests_mock: Mocker) -> None:
    """
    Tests that the ApiResolver returns a SERVFAIL error when the API call fails.
    """
    api_url = "http://test.com/q/"
    requests_mock.get(api_url, exc=requests.exceptions.ConnectionError)

    resolver = ApiResolver(api_url=api_url)
    request = DNSRecord.question("test question", qtype="TXT")

    response = resolver.resolve(request, handler=None)  # type: ignore

    assert len(response.rr) == 0
    assert response.header.rcode == 2  # RCODE 2 is SERVFAIL


def test_resolve_non_txt_query() -> None:
    """
    Tests that the ApiResolver returns a NOTIMP (Not Implemented)
    error for any query type other than TXT.
    """
    resolver = ApiResolver()
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
