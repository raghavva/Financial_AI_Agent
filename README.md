# Financial Agent (phidata)

A multi-agent financial analysis system that combines web search and financial data to provide comprehensive stock analysis and recommendations.

## Features

- **Web Search Agent**: Searches for recent financial news, filings, and analyst reports using DuckDuckGo
- **Financial Data Agent**: Retrieves 1-year price history, analyst recommendations, and company fundamentals using yfinance
- **Interactive Terminal Interface**: Prompts user for ticker symbol and optional custom analysis topic
- **Web Playground**: Optional web interface for testing agents individually

## Setup

1. **Create and activate a Python 3.10+ virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # Create .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

## Usage

### Interactive Terminal Mode (Recommended)
```bash
python financial_agent.py
```
- Enter ticker symbol when prompted (e.g., AAPL, MSFT, NVDA)
- Optionally provide a custom analysis topic or press Enter for default
- View comprehensive analysis with sources and data tables

### Web Playground Mode
```bash
python playground.py
```
- Access web interface at `http://localhost:8000`
- Test individual agents or run custom queries
- Useful for development and debugging

## Example Output

The system provides:
- **Recent News**: Latest financial news and analyst reports with source citations
- **Price Analysis**: 1-year historical data, volatility, and momentum metrics
- **Analyst Recommendations**: Current analyst consensus and price targets
- **Company Fundamentals**: Key financial metrics and company information
- **Data Sources**: All information includes proper citations and URLs

## Requirements

- Python 3.10+
- OpenAI API key
- Internet connection for web search and financial data

## Dependencies

- `phidata`: Multi-agent framework
- `openai`: GPT models
- `yfinance`: Financial data
- `duckduckgo-search`: Web search
- `rich`: Terminal formatting
- `fastapi` & `uvicorn`: Web playground (optional)

## Notes

- Requires `OPENAI_API_KEY` environment variable
- Uses GPT-4o-mini for cost efficiency (adjust model in code if needed)
- All data sources are properly cited with titles and URLs
- Analysis focuses on past 1-year timeframe for consistency


You can also directly run python playground.py and navigate to phidata's website and go the playground view.
