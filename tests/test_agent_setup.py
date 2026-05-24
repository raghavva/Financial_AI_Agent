import pytest
from financial_agent import web_search_agent, financial_agent, multi_agent


def test_web_search_agent_properties():
    agent = web_search_agent
    assert agent.name == "Web Search Agent"
    assert "Search the web" in agent.role
    assert any(tool.__class__.__name__ == "DuckDuckGo" for tool in agent.tools)
    assert any("Search broadly" in instr for instr in agent.instructions)
    assert agent.model is not None


def test_financial_agent_properties():
    agent = financial_agent
    assert agent.name == "Financial Data Agent"
    assert "Retrieve and analyze 1-year price data" in agent.role
    assert any(tool.__class__.__name__ == "YFinanceTools" for tool in agent.tools)
    assert any("Fetch 1-year historical" in instr for instr in agent.instructions)
    assert agent.model is not None


def test_multi_agent_team_and_instructions():
    agent = multi_agent
    assert len(agent.team) == 2
    names = {member.name for member in agent.team}
    assert "Web Search Agent" in names
    assert "Financial Data Agent" in names
    assert any("Always include data sources" in instr for instr in agent.instructions)
    assert agent.model is not None
