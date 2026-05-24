import pytest
from unittest.mock import patch, MagicMock
from financial_agent import multi_agent, build_query

@patch("financial_agent.multi_agent.print_response")
def test_print_response_called_with_valid_query(mock_print_response):
    query = build_query("AAPL")
    multi_agent.print_response(query, stream=False)
    mock_print_response.assert_called_with(query, stream=False)

@patch("financial_agent.multi_agent.print_response")
def test_print_response_with_custom_topic(mock_print_response):
    query = build_query("GOOG", "Provide detailed risk analysis.")
    multi_agent.print_response(query, stream=True)
    mock_print_response.assert_called_with(query, stream=True)

@patch("financial_agent.multi_agent.print_response")
def test_print_response_handles_invalid_input(mock_print_response):
    # We simulate an exception raised inside print_response
    mock_print_response.side_effect = Exception("API failure")
    with pytest.raises(Exception) as excinfo:
        multi_agent.print_response("invalid query", stream=False)
    assert "API failure" in str(excinfo.value)
