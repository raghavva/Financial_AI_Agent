from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv
from rich.console import Console
import sys

load_dotenv()

console = Console()

web_search_agent = Agent(
        name="Web Search Agent",
        role="Search the web for recent financial news and reports; include sources.",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[DuckDuckGo()],
        instructions=[
            "Search broadly across reputable sources from the past 1 year(news, filings, analyst notes).",
            "Always cite sources with titles and URLs.",
        ],
        show_tool_calls=True,
        markdown=True,
    )

financial_agent = Agent(
    name="Financial Data Agent",
        role="Retrieve and analyze 1-year price data, key stats, and analyst recs.",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[
            YFinanceTools(
                stock_price=True,
                analyst_recommendations=True,
                company_news=True,
                stock_fundamentals=True,
            )
        ],
        instructions=[
            "Fetch 1-year historical OHLC and compute drawdown, volatility, and momentum.",
            "Summarize analyst recommendations and company info concisely in tables.",
        ],
        show_tool_calls=True,
        markdown=True,
)

multi_agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    team=[web_search_agent, financial_agent],
    show_tool_calls=True,
    markdown=True,
    instructions=[
        "Always include data sources in the output.",
        "Use tables to display the data."
    ],
)


def build_query(ticker: str, topic: str | None = None) -> str:
    base = f"Summarize analyst recommendations and share the latest news for {ticker}."
    return topic if topic else base


def is_valid_ticker(ticker: str) -> bool:
    """Validate ticker by attempting to fetch basic info using YFinanceTools without side effects."""
    yf_tool = YFinanceTools()
    try:
        info = yf_tool.get_company_info(ticker)
        # get_company_info returns dict with keys if valid, empty or error if invalid
        if info and isinstance(info, dict) and len(info) > 0:
            return True
        return False
    except Exception:
        # Treat exceptions here as invalid ticker
        return False


def main():
    load_dotenv()
    ticker = input("Enter ticker (e.g., AAPL): ").strip().upper()
    if not ticker:
        console.print(":cross_mark: [bold red]Error:[/bold red] Ticker input cannot be empty. Please provide a valid ticker symbol.")
        return

    if not is_valid_ticker(ticker):
        console.print(f":cross_mark: [bold red]Error:[/bold red] The ticker symbol '{ticker}' is invalid or not recognized. Please check and try again.")
        return

    raw = input("Optional topic (press Enter to use default): ").strip()
    topic = raw if raw else None
    query = build_query(ticker, topic)

    try:
        multi_agent.print_response(query, stream=True)
    except Exception as e:
        err_msg = str(e)
        # Determine if error is likely from yfinance or duckduckgo tools
        if "yfinance" in err_msg.lower():
            console.print(":cross_mark: [bold red]Error:[/bold red] Failed to retrieve financial data from yfinance. Please check your internet connection and ticker symbol.")
        elif "duckduckgo" in err_msg.lower() or "duckduckgo_search" in err_msg.lower():
            console.print(":cross_mark: [bold red]Error:[/bold red] Web search service failed. Please try again later.")
        else:
            console.print(f":cross_mark: [bold red]Error:[/bold red] An unexpected error occurred: {err_msg}")


if __name__ == "__main__":
    main()
