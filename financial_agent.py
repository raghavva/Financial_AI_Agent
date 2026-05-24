from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv
import json
from typing import Optional, Union

load_dotenv()


# Helper function to convert response to JSON schema
# Assuming the agent's internal response can be parsed to extract structured data
# Placeholder JSON structure, real structure depends on agent's response parsing

def to_json_output(response_text: str) -> dict:
    # Dummy implementation: attempt to parse known sections from the markdown
    # For real apps, one might parse the model output or have agents generate JSON directly.
    # Here, we simulate a basic structure
    # Users should adapt this function based on the actual response format
    return {
        "summary": response_text,
        "metadata": {
            "format": "json_output",
            "source": "Financial_AI_Agent",
        }
    }


class OutputFormat:
    MARKDOWN = 'markdown'
    JSON = 'json'


class ExtendedAgent(Agent):
    def __init__(self, *args, output_format: str = OutputFormat.MARKDOWN, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_format = output_format

    def get_response(self, query: str, stream: bool = False) -> Union[str, dict]:
        # Call super().get_response, but convert output depending on format
        result = super().get_response(query, stream=stream)
        if self.output_format == OutputFormat.JSON:
            # Convert markdown string result to JSON schema
            if isinstance(result, str):
                return to_json_output(result)
            # if other types returned, pass as-is
            return result
        else:
            return result

    def print_response(self, query: str, stream: bool = False):
        response = self.get_response(query, stream=stream)
        if self.output_format == OutputFormat.JSON:
            print(json.dumps(response, indent=2))
        else:
            print(response)


web_search_agent = ExtendedAgent(
        name="Web Search Agent",
        role="Search the web for recent financial news and reports; include sources.",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[DuckDuckGo()],
        instructions=[
            "Search broadly across reputable sources from the past 1 year(news, filings, analyst notes).",
            "Always cite sources with titles and URLs.",
        ],
        show_tool_calls=True,
        output_format=OutputFormat.MARKDOWN,
    )

financial_agent = ExtendedAgent(
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
        output_format=OutputFormat.MARKDOWN,
)

multi_agent = ExtendedAgent(
    model=OpenAIChat(id="gpt-4o-mini"),
    team=[web_search_agent, financial_agent],
    show_tool_calls=True,
    output_format=OutputFormat.MARKDOWN,
    instructions=[
        "Always include data sources in the output.",
        "Use tables to display the data."
    ],
)


def build_query(ticker: str, topic: Optional[str] = None) -> str:
    base = f"Summarize analyst recommendations and share the latest news for {ticker}."
    return topic if topic else base


def main():
    load_dotenv()
    ticker = input("Enter ticker (e.g., AAPL): ").strip().upper()
    raw = input("Optional topic (press Enter to use default): ").strip()
    topic = raw if raw else None
    output_format = input("Choose output format (markdown/json) [markdown]: ").strip().lower() or "markdown"
    if output_format not in [OutputFormat.MARKDOWN, OutputFormat.JSON]:
        print(f"Unknown output format '{output_format}', falling back to markdown.")
        output_format = OutputFormat.MARKDOWN

    # Rebuild agents to set output_format accordingly
    web_search_agent.output_format = output_format
    financial_agent.output_format = output_format
    multi_agent.output_format = output_format

    query = build_query(ticker, topic)
    multi_agent.print_response(query, stream=True)


if __name__ == "__main__":
    main()
