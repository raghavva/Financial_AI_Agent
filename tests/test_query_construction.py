import pytest
from financial_agent import build_query

@pytest.mark.parametrize("ticker, topic, expected", [
    ("AAPL", None, "Summarize analyst recommendations and share the latest news for AAPL."),
    ("TSLA", "Custom topic on EV market", "Custom topic on EV market"),
    ("GOOGL", "", "Summarize analyst recommendations and share the latest news for GOOGL."),
    ("MSFT", "Recent acquisitions", "Recent acquisitions"),
])
def test_build_query(ticker, topic, expected):
    result = build_query(ticker, topic)
    assert result == expected

@pytest.mark.parametrize("topic", [None, "Some specialized topic"])
def test_build_query_default_behavior(topic):
    ticker = "IBM"
    expected = topic if topic else f"Summarize analyst recommendations and share the latest news for {ticker}."
    assert build_query(ticker, topic) == expected
