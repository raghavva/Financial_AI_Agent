import pytest
from financial_agent import build_query

@pytest.mark.parametrize("ticker,topic,expected", [
    ("AAPL", None, "Summarize analyst recommendations and share the latest news for AAPL."),
    ("TSLA", "What are Tesla's recent earnings?", "What are Tesla's recent earnings?"),
    ("GOOG", "", "Summarize analyst recommendations and share the latest news for GOOG."),
    ("MSFT", "Summarize Microsoft Q1 results.", "Summarize Microsoft Q1 results."),
])
def test_build_query_various_inputs(ticker, topic, expected):
    result = build_query(ticker, topic)
    assert result == expected

@pytest.mark.parametrize("ticker", ["", " ", None])
def test_build_query_empty_or_none_ticker(ticker):
    # When ticker is empty, base string uses it verbatim
    result = build_query(ticker)
    assert isinstance(result, str)
    if ticker is None:
        assert result == "Summarize analyst recommendations and share the latest news for None."
    else:
        assert ticker.strip() in result
