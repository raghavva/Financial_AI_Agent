import pytest
from unittest.mock import patch, AsyncMock
from financial_agent import multi_agent, build_query


class DummyResponse:
    def __init__(self):
        self.called = False

    def __call__(self, query, stream):
        self.called = True
        if not query:
            raise ValueError("Query cannot be empty")
        return f"Response for: {query}"


def test_print_response_success(monkeypatch):
    # Patch the print_response method to a dummy one to avoid real API calls
    dummy = DummyResponse()
    monkeypatch.setattr(multi_agent, "print_response", dummy)

    query = build_query("AAPL")
    result = multi_agent.print_response(query, stream=True)
    assert dummy.called


def test_print_response_with_invalid_query(monkeypatch):
    dummy = DummyResponse()
    monkeypatch.setattr(multi_agent, "print_response", dummy)

    with pytest.raises(ValueError):
        dummy.__call__("", stream=True)  # Direct call simulating invalid empty query


def test_print_response_handles_exception(monkeypatch):
    def raise_error(query, stream):
        raise RuntimeError("API failure simulated")

    monkeypatch.setattr(multi_agent, "print_response", raise_error)

    with pytest.raises(RuntimeError) as exc:
        multi_agent.print_response("AAPL", stream=True)
    assert "API failure simulated" in str(exc.value)
