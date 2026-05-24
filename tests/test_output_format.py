import pytest
from financial_agent import ExtendedAgent, OutputFormat, to_json_output

class DummyAgent(ExtendedAgent):
    def get_response(self, query: str, stream: bool = False):
        # Return a fixed simulated markdown response to test json conversion
        # For JSON mode, convert markdown to JSON format
        base_response = ("# Summary\nThis is a test analysis for {query}.\n"
                         "\nData sources: Example Source.\n".format(query=query))
        if self.output_format == OutputFormat.JSON:
            return to_json_output(base_response)
        else:
            return base_response

def test_markdown_output():
    agent = DummyAgent(name="test", role="", model=None, tools=[], output_format=OutputFormat.MARKDOWN)
    response = agent.get_response("AAPL")
    assert isinstance(response, str)
    assert "Summary" in response


def test_json_output():
    agent = DummyAgent(name="test", role="", model=None, tools=[], output_format=OutputFormat.JSON)
    response = agent.get_response("AAPL")
    assert isinstance(response, dict)
    assert "summary" in response
    assert isinstance(response["summary"], str)
    assert response["metadata"]["format"] == "json_output"


def test_to_json_output_basic():
    text = "# Example\nTest content"
    json_data = to_json_output(text)
    assert isinstance(json_data, dict)
    assert "summary" in json_data
    assert json_data["summary"] == text
    assert "metadata" in json_data
    assert json_data["metadata"]["source"] == "Financial_AI_Agent"


if __name__ == "__main__":
    pytest.main()
