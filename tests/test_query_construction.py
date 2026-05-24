import pytest
from financial_agent import build_query

def test_build_query_default():
    ticker = "AAPL"
    expected = f"Summarize analyst recommendations and share the latest news for {ticker}."
    assert build_query(ticker) == expected

@ pytest.mark.parametrize("ticker,topic,expected", [
    ("TSLA", None, "Summarize analyst recommendations and share the latest news for TSLA."),
    ("MSFT", "Provide detailed risk analysis.", "Provide detailed risk analysis."),
    ("GOOG", "", ""),
])
def test_build_query_various_inputs(ticker, topic, expected):
    assert build_query(ticker, topic) == expected
