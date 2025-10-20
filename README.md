# Smart Portfolio Agent (CapitalCube)

AI-powered investment allocation tool that generates intelligent portfolio diversification recommendations based on a target ticker, investment amount, and risk tolerance using CapitalCube's peer group analysis and earnings quality scoring.

## 🎯 Overview

Given a ticker, budget (e.g., $10K), and risk level, the agent allocates funds across 3-5 peer companies or ETFs and generates a summary of expected returns and risk.

**Key Features:**
- ✅ Risk-adjusted portfolio allocation (Low/Medium/High)
- ✅ Earnings Quality Scores (1-5 scale) derived from CapitalCube analytics
- ✅ Peer company discovery via CapitalCube reports
- ✅ LLM-generated allocation rationale
- ✅ Sector diversification analysis
- ✅ ETF inclusion for tail risk mitigation

## 🏗️ Architecture

Multi-agent system built with **LangGraph** and **FastAPI**:

```
Peer Research Agent → Scoring Agent → Allocation Agent → Summary Agent
```

1. **Peer Research Agent**: Discovers peer companies from CapitalCube reports
2. **Scoring Agent**: Calculates earnings quality scores (1-5)
3. **Allocation Agent**: Applies risk-based allocation algorithms
4. **Summary Agent**: Generates human-readable rationale (GPT-4)

## 📋 Requirements

- Python 3.11+
- OpenAI API key (for LLM)
- CapitalCube access (reports or API)
- Optional: Arize account for observability

## 🚀 Quick Start

### 1. Clone & Setup
```bash
cd smart-portfolio-agent
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 2. Configure Environment
```bash
cp backend/.env.example backend/.env
# Edit .env with your API keys
```

### 3. Run the Server
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 4. Test the API
```bash
curl -X POST http://localhost:8000/api/v1/portfolio/generate \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "investment_amount": 10000,
    "risk_level": "medium",
    "include_etfs": true,
    "max_holdings": 5
  }'
```

## 📊 Example Output

**Input:** AAPL, $10K, Medium Risk

**Output:**
```json
{
  "allocation": [
    {"ticker": "AAPL", "allocation_percent": 35, "amount": 3500, "score": 4.2},
    {"ticker": "MSFT", "allocation_percent": 30, "amount": 3000, "score": 4.5},
    {"ticker": "GOOGL", "allocation_percent": 20, "amount": 2000, "score": 3.8},
    {"ticker": "AVGO", "allocation_percent": 10, "amount": 1000, "score": 4.0},
    {"ticker": "XLK", "allocation_percent": 5, "amount": 500, "score": null}
  ],
  "summary": {
    "total_holdings": 5,
    "average_earnings_quality": 4.1,
    "risk_profile": "moderate"
  },
  "rationale": "This allocation prioritizes quality mega-cap technology companies..."
}
```

## 📁 Project Structure

```
smart-portfolio-agent/
├── backend/
│   ├── agents/
│   │   └── portfolio_agent.py       # 4-agent LangGraph workflow
│   ├── tools/
│   │   ├── capitalcube_parser.py    # PDF parsing
│   │   ├── allocation_algorithms.py # Risk-based allocation
│   │   └── market_data.py           # Yahoo Finance integration
│   ├── data/
│   │   ├── capitalcube_cache/       # Cached reports (7-day TTL)
│   │   ├── sector_mappings.json     # GICS classifications
│   │   └── etf_database.json        # Sector ETF metadata
│   ├── config/
│   │   └── portfolio_config.yaml    # Risk parameters
│   ├── main.py                      # FastAPI app
│   ├── requirements.txt
│   └── .env
├── frontend/
│   └── portfolio.html               # Web UI
├── sample-data/
│   ├── README.md
│   └── Valisha---EarningsQuality-HOOD-US-10-18-2025.pdf
├── tests/
│   ├── test_allocation.py
│   ├── test_portfolio_agent.py
│   └── test_capitalcube_parser.py
├── SMART_PORTFOLIO_AGENT_PRD.md     # Full product spec
├── PORTFOLIO_AGENT_FLOW.md          # Agent implementation guide
└── README.md
```

## 🔑 Environment Variables

Create `backend/.env`:

```bash
# LLM Provider
OPENAI_API_KEY=your_openai_key_here

# CapitalCube (if API available)
CAPITALCUBE_API_KEY=your_capitalcube_key

# Market Data
YAHOO_FINANCE_API_KEY=optional

# Caching
REDIS_URL=redis://localhost:6379

# Observability (optional)
ARIZE_SPACE_ID=your_arize_space_id
ARIZE_API_KEY=your_arize_api_key

# Rate Limiting
RATE_LIMIT_PER_HOUR=20
MAX_CACHE_TTL_SECONDS=604800  # 7 days
```

## 🎨 Risk Levels

| Level | Strategy | Max Single Stock | Profile |
|-------|----------|------------------|---------|
| **Low** | Conservative, ETF-heavy | 25% | Equal-weight + 50% ETFs |
| **Medium** | Balanced quality-weighted | 35% | Quality scores drive allocation |
| **High** | Concentrated conviction | 50% | Top holding 40-50% |

## 📈 Earnings Quality Score

**1-5 Scale** derived from CapitalCube analytics:

- **4.5-5.0**: Elite - Conservative accounting, strong fundamentals
- **3.5-4.4**: Strong - Solid with minor concerns
- **2.5-3.4**: Average - Multiple red flags
- **1.0-2.4**: Weak - Significant issues

**Based on:**
- Net margins vs. peer median
- Accruals analysis (earnings quality)
- Accounting quality classification
- Potential issues count (11 categories)

## 🧪 Testing

```bash
# Unit tests
pytest tests/test_allocation.py

# Integration tests
pytest tests/test_portfolio_agent.py

# Test with real ticker
curl -X POST http://localhost:8000/api/v1/portfolio/generate \
  -H "Content-Type: application/json" \
  -d '{"ticker": "HOOD", "investment_amount": 10000, "risk_level": "medium"}'
```

## 📚 Documentation

- **[PRD](SMART_PORTFOLIO_AGENT_PRD.md)**: Complete product specification
- **[Agent Flow](PORTFOLIO_AGENT_FLOW.md)**: Implementation guide with code examples
- **[Sample Data](sample-data/)**: Reference CapitalCube reports

## 🚧 Development Status

**Phase 1: MVP** (Weeks 1-3)
- [ ] CapitalCube PDF parser
- [ ] 4-agent LangGraph workflow
- [ ] Risk-based allocation algorithms
- [ ] FastAPI endpoints
- [ ] Basic web UI

**Phase 2: Enhancement** (Weeks 4-5)
- [ ] Redis caching
- [ ] Comparison endpoint (3 risk levels)
- [ ] Enhanced error handling
- [ ] Arize observability

**Phase 3: Production** (Weeks 6-8)
- [ ] Load testing
- [ ] Security audit
- [ ] Documentation
- [ ] Deployment (Render.com)

## 🤝 Contributing

This is a separate application from the AI Trip Planner (Smart Budget Agent). While it shares architectural patterns (LangGraph, FastAPI), it focuses on financial portfolio allocation rather than travel planning.

## ⚖️ Disclaimer

**This tool is for informational purposes only and does not constitute investment advice.** Past performance does not guarantee future results. All investments carry risk of loss. Consult a licensed financial advisor before making investment decisions.

## 📝 License

MIT License

---

**Built with:** LangGraph • FastAPI • OpenAI • CapitalCube • Yahoo Finance

