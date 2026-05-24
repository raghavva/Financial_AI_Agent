from phi.playground import Playground, serve_playground_app
from financial_agent import financial_agent as base_financial_agent, web_search_agent as base_web_search_agent, OutputFormat, ExtendedAgent
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

load_dotenv()


# Provide ability to select output format here
# For demonstration, default to markdown but allow JSON via playground config or environment

# For playground use, we expose JSON output format as option by wrapping agents


class PlaygroundAgentWrapper(ExtendedAgent):
    def __init__(self, base_agent: ExtendedAgent, output_format: str):
        super().__init__(
            name=base_agent.name,
            role=base_agent.role,
            model=base_agent.model,
            tools=base_agent.tools,
            instructions=base_agent.instructions,
            show_tool_calls=base_agent.show_tool_calls,
            output_format=output_format
        )


# Setup agents for playground: supporting markdown and json output

financial_agent_markdown = PlaygroundAgentWrapper(base_financial_agent, OutputFormat.MARKDOWN)
financial_agent_json = PlaygroundAgentWrapper(base_financial_agent, OutputFormat.JSON)

web_search_agent_markdown = PlaygroundAgentWrapper(base_web_search_agent, OutputFormat.MARKDOWN)
web_search_agent_json = PlaygroundAgentWrapper(base_web_search_agent, OutputFormat.JSON)

# For playground demonstration we choose default as markdown
app = Playground(agents=[financial_agent_markdown, web_search_agent_markdown, financial_agent_json, web_search_agent_json]).get_app()


if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)
