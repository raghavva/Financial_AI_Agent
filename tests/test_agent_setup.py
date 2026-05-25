import pytest
from financial_agent import web_search_agent, financial_agent, multi_agent


def test_web_search_agent_properties():
    assert web_search_agent.name == "Web Search Agent"
    assert "Search the web" in web_search_agent.role
    assert len(web_search_agent.tools) == 1
    assert web_search_agent.tools[0].__class__.__name__ == "DuckDuckGo"
    assert web_search_agent.model.__class__.__name__ == "OpenAIChat"
    assert isinstance(web_search_agent.instructions, list)
    assert web_search_agent.show_tool_calls is True
    assert web_search_agent.markdown is True


def test_financial_agent_properties():
    assert financial_agent.name == "Financial Data Agent"
    assert "Retrieve and analyze" in financial_agent.role
    assert len(financial_agent.tools) == 1
    tools_class_names = [t.__class__.__name__ for t in financial_agent.tools]
    assert "YFinanceTools" in tools_class_names
    assert financial_agent.model.__class__.__name__ == "OpenAIChat"
    assert isinstance(financial_agent.instructions, list)
    assert financial_agent.show_tool_calls is True
    assert financial_agent.markdown is True


def test_multi_agent_team_and_properties():
    team_agents = multi_agent.team
    assert any(agent.name == "Web Search Agent" for agent in team_agents)
    assert any(agent.name == "Financial Data Agent" for agent in team_agents)
    assert all(agent.__class__.__name__ == "Agent" for agent in team_agents)
    assert multi_agent.model.__class__.__name__ == "OpenAIChat"
    assert "Always include data sources" in " ".join(multi_agent.instructions)
    assert multi_agent.show_tool_calls is True
    assert multi_agent.markdown is True
