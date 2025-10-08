from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

load_dotenv()

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

def main():
    load_dotenv()
    ticker = input("Enter ticker (e.g., AAPL): ").strip().upper()
    raw = input("Optional topic (press Enter to use default): ").strip()
    topic = raw if raw else None
    query = build_query(ticker, topic)
    multi_agent.print_response(query, stream=True)

if __name__ == "__main__":
    main()