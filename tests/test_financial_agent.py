import pytest
from unittest.mock import patch, MagicMock
import builtins
from financial_agent import main
from io import StringIO
from rich.console import Console

console = Console()


@patch('builtins.input', side_effect=['', ''])
@patch('rich.console.Console.print')
def test_empty_ticker_input(mock_print, mock_input):
    main()
    mock_print.assert_any_call(":cross_mark: [bold red]Error:[/bold red] Ticker input cannot be empty. Please provide a valid ticker symbol.")


@patch('financial_agent.YFinanceTools.get_company_info', return_value={})
@patch('builtins.input', side_effect=['INVALIDTICKER', ''])
@patch('rich.console.Console.print')
def test_invalid_ticker_symbol(mock_print, mock_input, mock_get_info):
    main()
    mock_print.assert_any_call(":cross_mark: [bold red]Error:[/bold red] The ticker symbol 'INVALIDTICKER' is invalid or not recognized. Please check and try again.")


@patch('financial_agent.YFinanceTools.get_company_info', side_effect=Exception("Network error"))
@patch('builtins.input', side_effect=['FAKE', ''])
@patch('rich.console.Console.print')
def test_ticker_validation_exception(mock_print, mock_input, mock_get_info):
    main()
    mock_print.assert_any_call(":cross_mark: [bold red]Error:[/bold red] The ticker symbol 'FAKE' is invalid or not recognized. Please check and try again.")


@patch('financial_agent.YFinanceTools.get_company_info', return_value={'symbol': 'AAPL'})
@patch('builtins.input', side_effect=['AAPL', ''])
@patch('financial_agent.multi_agent.print_response')
def test_valid_ticker_runs_agent(mock_print_response, mock_input, mock_get_info):
    mock_print_response.side_effect = lambda query, stream: print(f"Running agent with query: {query}")
    main()
    mock_print_response.assert_called_once()


@patch('financial_agent.YFinanceTools.get_company_info', return_value={'symbol': 'AAPL'})
@patch('builtins.input', side_effect=['AAPL', ''])
@patch('financial_agent.multi_agent.print_response')
@patch('rich.console.Console.print')
def test_agent_raises_yfinance_error(mock_console_print, mock_print_response, mock_input, mock_get_info):
    mock_print_response.side_effect = Exception("Error from yfinance service")
    main()
    mock_console_print.assert_any_call(":cross_mark: [bold red]Error:[/bold red] Failed to retrieve financial data from yfinance. Please check your internet connection and ticker symbol.")


@patch('financial_agent.YFinanceTools.get_company_info', return_value={'symbol': 'AAPL'})
@patch('builtins.input', side_effect=['AAPL', ''])
@patch('financial_agent.multi_agent.print_response')
@patch('rich.console.Console.print')
def test_agent_raises_duckduckgo_error(mock_console_print, mock_print_response, mock_input, mock_get_info):
    mock_print_response.side_effect = Exception("DuckDuckGo_search failed")
    main()
    mock_console_print.assert_any_call(":cross_mark: [bold red]Error:[/bold red] Web search service failed. Please try again later.")


@patch('financial_agent.YFinanceTools.get_company_info', return_value={'symbol': 'AAPL'})
@patch('builtins.input', side_effect=['AAPL', ''])
@patch('financial_agent.multi_agent.print_response')
@patch('rich.console.Console.print')
def test_agent_raises_unknown_error(mock_console_print, mock_print_response, mock_input, mock_get_info):
    mock_print_response.side_effect = Exception("Some unknown error")
    main()
    mock_console_print.assert_any_call(":cross_mark: [bold red]Error:[/bold red] An unexpected error occurred: Some unknown error")
