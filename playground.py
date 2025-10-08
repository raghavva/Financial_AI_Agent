from phi.playground import Playground, serve_playground_app
from financial_agent import financial_agent, web_search_agent
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


app = Playground(agents=[financial_agent, web_search_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)