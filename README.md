## Financial Agent (phidata)

### Setup
1. Create and activate a Python 3.10+ venv.
2. Install deps:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy env and set keys:
   ```bash
   cp .env.sample .env
   # edit .env with your OPENAI_API_KEY, TICKER, TOPIC
   ```

### Run
```bash
python run.py
```

### What it does
- Web Search Agent: uses DuckDuckGo to gather recent sources and cites links.
- Financial Data Agent: pulls 1-year price stats and analyst recs via yfinance tools.
- Manager Agent: synthesizes a concise report and outputs BUY/HOLD with rationale.

### Notes
- Requires `OPENAI_API_KEY` for OpenAI models used by phidata.
- Adjust model IDs in `agents/*.py` if needed.


