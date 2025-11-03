# 🚀 Smart Portfolio Agent - Getting Started

Welcome to the Smart Portfolio Agent! This guide will help you set up and run the application.

## ✅ What's Been Created

Your new project directory is ready at:
```
/Users/valishagravesnew/Cursor/smart-portfolio-agent/
```

**Project Structure:**
```
smart-portfolio-agent/
├── 📄 README.md                          # Main documentation
├── 📄 SMART_PORTFOLIO_AGENT_PRD.md       # Complete product spec
├── 📄 PORTFOLIO_AGENT_FLOW.md            # Agent implementation guide
├── 📄 START_HERE.md                      # This file!
├── 📄 .gitignore                         # Git ignore rules
│
├── backend/
│   ├── main.py                           # ✅ FastAPI app (placeholder)
│   ├── requirements.txt                  # ✅ Python dependencies
│   ├── .env.example                      # ✅ Environment template
│   ├── agents/
│   │   ├── __init__.py
│   │   └── portfolio_agent.py            # ✅ 4-agent workflow (stub)
│   ├── tools/
│   │   └── __init__.py
│   ├── data/
│   │   └── capitalcube_cache/
│   └── config/
│
├── frontend/
│   └── (portfolio.html to be created)
│
├── sample-data/
│   ├── README.md                         # ✅ Sample data documentation
│   └── Valisha---EarningsQuality-HOOD-US-10-18-2025.pdf  # ✅ Reference report
│
└── tests/
    └── (test files to be created)
```

## 🎯 Quick Start (5 Minutes)

### 1. Navigate to Project
```bash
cd /Users/valishagravesnew/Cursor/smart-portfolio-agent
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Configure Environment
```bash
cd backend
nano .env  # Create and edit .env file
```

**Add your API keys to `.env`:**
```bash
# Required
OPENAI_API_KEY=sk-your-openai-key-here

# Recommended: Arize Tracing (see TRACING_QUICK_START.md)
ARIZE_SPACE_ID=your-arize-space-id-here
ARIZE_API_KEY=your-arize-api-key-here
ARIZE_PROJECT_NAME=smart-portfolio-agent

# Optional (for future implementation)
CAPITALCUBE_API_KEY=your_key_here
REDIS_URL=redis://localhost:6379
```

**Note**: For Arize tracing setup, see **[TRACING_QUICK_START.md](TRACING_QUICK_START.md)** (2 minutes)

### 5. Run the Server
```bash
# From backend/ directory
python main.py

# Or with uvicorn
uvicorn main:app --reload --port 8000
```

### 6. Test the API
Open your browser to:
- **Swagger UI:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

Or use curl:
```bash
curl http://localhost:8000/health
```

## 📊 Test the Portfolio Endpoint

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

**Note:** The current implementation returns placeholder data. The full agent workflow needs to be implemented according to `PORTFOLIO_AGENT_FLOW.md`.

## 🔧 Implementation Status

### ✅ Completed
- [x] Project structure created
- [x] Documentation (PRD + Agent Flow)
- [x] FastAPI skeleton
- [x] Request/response models
- [x] Sample CapitalCube report
- [x] Dependencies listed
- [x] Environment configuration

### 🚧 To Be Implemented

**Phase 1: Core Agents** (see `PORTFOLIO_AGENT_FLOW.md`)
- [ ] Peer Research Agent
  - [ ] CapitalCube PDF parser (`tools/capitalcube_parser.py`)
  - [ ] Sector-based peer discovery fallback
- [ ] Scoring Agent
  - [ ] Quality score calculation algorithm
  - [ ] Yahoo Finance market data integration
- [ ] Allocation Agent
  - [ ] Low risk algorithm (`tools/allocation_algorithms.py`)
  - [ ] Medium risk algorithm
  - [ ] High risk algorithm
- [ ] Summary Agent
  - [ ] LLM prompt engineering
  - [ ] Rationale generation

**Phase 2: Data Integration**
- [ ] CapitalCube report parser
- [ ] Yahoo Finance API wrapper
- [ ] Redis caching layer
- [ ] ETF database

**Phase 3: Frontend**
- [ ] Web UI (`frontend/portfolio.html`)
- [ ] Allocation visualization
- [ ] Risk comparison view

## 📚 Key Documentation

1. **[SMART_PORTFOLIO_AGENT_PRD.md](SMART_PORTFOLIO_AGENT_PRD.md)**
   - Complete product requirements
   - Feature specifications (F1-F4)
   - API endpoints
   - Risk levels & scoring system

2. **[PORTFOLIO_AGENT_FLOW.md](PORTFOLIO_AGENT_FLOW.md)**
   - 4-agent implementation guide
   - Complete code examples
   - State management
   - Tool implementations

3. **[TRACING_QUICK_START.md](TRACING_QUICK_START.md)** ⭐ NEW
   - 2-minute Arize tracing setup
   - Monitor LLM performance & costs
   - Debug agent workflows

4. **[ARIZE_TRACING_SETUP.md](ARIZE_TRACING_SETUP.md)**
   - Detailed tracing configuration
   - Advanced features & troubleshooting

5. **[sample-data/README.md](sample-data/README.md)**
   - CapitalCube report structure
   - Data extraction examples
   - Parser testing guide

## 🛠️ Next Steps for Development

### Immediate Priorities

1. **Implement PDF Parser** (1-2 days)
   ```bash
   # Create the parser
   touch backend/tools/capitalcube_parser.py
   
   # Test with sample HOOD report
   pytest tests/test_capitalcube_parser.py
   ```

2. **Implement Scoring Logic** (1-2 days)
   ```bash
   # Create scoring calculator
   touch backend/tools/scoring.py
   
   # Use formula from PRD Section F3
   ```

3. **Implement Allocation Algorithms** (1-2 days)
   ```bash
   # Create allocation module
   touch backend/tools/allocation_algorithms.py
   
   # Implement 3 risk-level algorithms (PRD Section 11.1)
   ```

4. **Connect LangGraph Agents** (2-3 days)
   - Update `backend/agents/portfolio_agent.py`
   - Wire up all 4 agents
   - Test end-to-end flow

### Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/pdf-parser

# 2. Implement feature
# (edit files)

# 3. Test
pytest tests/

# 4. Run locally
cd backend && python main.py

# 5. Test endpoint
curl -X POST http://localhost:8000/api/v1/portfolio/generate -H "Content-Type: application/json" -d '{...}'

# 6. Commit
git add .
git commit -m "feat: implement CapitalCube PDF parser"
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_allocation.py

# Run with coverage
pytest --cov=backend --cov-report=html
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'langgraph'"
```bash
pip install -r backend/requirements.txt
```

### "OpenAI API key not found"
```bash
# Check .env file exists
ls backend/.env

# Edit and add your key
nano backend/.env
```

### "Redis connection failed"
```bash
# Redis is optional for MVP
# Comment out Redis in .env or install Redis:
brew install redis  # macOS
brew services start redis
```

## 📦 Deployment

When ready for production:

1. Update `render.yaml` (similar to trip planner)
2. Set environment variables in Render dashboard
3. Deploy to Render.com

## 🤝 Relationship to Trip Planner

This is a **separate application** from the AI Trip Planner (Smart Budget Agent):

| Trip Planner | Portfolio Agent |
|--------------|-----------------|
| Located: `ai-trip-planner/` | Located: `smart-portfolio-agent/` |
| Domain: Travel planning | Domain: Financial portfolio allocation |
| Data: Weather, hotels, attractions | Data: CapitalCube, stock prices |
| Output: Travel itinerary | Output: Investment allocation |

**Shared patterns:**
- Both use LangGraph + FastAPI architecture
- Both implement multi-agent workflows
- Both use OpenAI for LLM reasoning
- Both have observability via Arize

## 💡 Tips

1. **Start with the PDF parser** - It's the foundation for everything
2. **Test with HOOD sample report** - Use the provided CapitalCube report
3. **Implement medium risk first** - It's the most common use case
4. **Use placeholders initially** - Get the flow working, then add real APIs
5. **Refer to agent flow doc** - It has complete code examples

## 🎓 Learning Resources

- **LangGraph Tutorial:** https://langchain-ai.github.io/langgraph/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **CapitalCube Sample:** `sample-data/Valisha---EarningsQuality-HOOD-US-10-18-2025.pdf`

---

## ✨ Ready to Code?

```bash
# Open the project in VS Code or Cursor
code /Users/valishagravesnew/Cursor/smart-portfolio-agent

# Start implementing!
# Begin with: backend/tools/capitalcube_parser.py
```

**Good luck! 🚀**

For questions, refer to:
- `SMART_PORTFOLIO_AGENT_PRD.md` - What to build
- `PORTFOLIO_AGENT_FLOW.md` - How to build it




