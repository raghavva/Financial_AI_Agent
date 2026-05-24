import pytest
from financial_agent import web_search_agent, financial_agent, multi_agent


def test_web_search_agent_properties():
    assert web_search_agent.name == "Web Search Agent"
    assert "Search the web" in web_search_agent.role
    assert any(tool.__class__.__name__ == "DuckDuckGo" for tool in web_search_agent.tools)
    assert "Always cite sources" in web_search_agent.instructions[1]
    assert web_search_agent.show_tool_calls is True
    assert web_search_agent.markdown is True


def test_financial_agent_properties():
    assert financial_agent.name == "Financial Data Agent"
    assert "Retrieve and analyze" in financial_agent.role
    tools_names = [tool.__class__.__name__ for tool in financial_agent.tools]
    assert "YFinanceTools" in tools_names
    instructions = financial_agent.instructions
    assert any("historical OHLC" in instr for instr in instructions)
    assert financial_agent.show_tool_calls is True
    assert financial_agent.markdown is True


def test_multi_agent_properties():
    # multi_agent has no explicit name, but has model and team
    assert multi_agent.model is not None
    assert hasattr(multi_agent, "team")
    team_names = [agent.name for agent in multi_agent.team]
    assert "Web Search Agent" in team_names
    assert "Financial Data Agent" in team_names
    assert multi_agent.show_tool_calls is True
    assert multi_agent.markdown is True
    assert any("Always include data sources" in instr for instr in multi_agent.instructions)
