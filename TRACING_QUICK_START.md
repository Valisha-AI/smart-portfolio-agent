# 🚀 Arize Tracing - Quick Start

## ⚡ 2-Minute Setup

### 1. Get Arize API Keys
Visit [app.arize.com](https://app.arize.com) → Settings → API Keys

### 2. Create `.env` file
```bash
cd backend
cat > .env << 'EOF'
# Required
OPENAI_API_KEY=sk-your-openai-key-here
ARIZE_SPACE_ID=your-arize-space-id-here
ARIZE_API_KEY=your-arize-api-key-here
ARIZE_PROJECT_NAME=smart-portfolio-agent

# Optional
CAPITALCUBE_API_KEY=your-capitalcube-key-here
REDIS_URL=redis://localhost:6379
ENVIRONMENT=development
EOF
```

**Edit the file** with your actual API keys:
```bash
nano .env  # or use your favorite editor
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start Server
```bash
python main.py
```

Look for: `🔍 Arize Tracing: ✅ Enabled`

### 5. Test It
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

### 6. View Traces
Go to [app.arize.com](https://app.arize.com) → Tracing

---

## ✅ What's Instrumented?

- ✅ **LangGraph agent workflows** (peer research, scoring, allocation, summary)
- ✅ **OpenAI API calls** (GPT-4 prompts, responses, tokens, costs)
- ✅ **Tool executions** (Yahoo Finance, scoring algorithms)
- ✅ **Request metadata** (ticker, amount, risk level)
- ✅ **Errors & exceptions** (full stack traces)

---

## 📊 What You'll See in Arize

### Per Request
- Full trace timeline (agent → tools → LLM)
- Token usage & costs
- Latency breakdown
- Prompt & response content
- Tool results (stock data, scores)

### Dashboards
- Average response time
- Total requests
- Error rates
- Daily OpenAI costs
- Most common tickers

---

## 🔧 Verify Setup

### Check Health Endpoint
```bash
curl http://localhost:8000/health | jq
```

Should show:
```json
{
  "tracing": {
    "enabled": true,
    "project_name": "smart-portfolio-agent"
  }
}
```

### Check Server Logs
```
✅ Arize tracing initialized successfully for project: smart-portfolio-agent
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `⚠️ Not configured` | Set `ARIZE_SPACE_ID` and `ARIZE_API_KEY` in `.env` |
| `Failed to import` | Run `pip install -r requirements.txt` |
| No traces in Arize | Wait 1-2 minutes, check credentials, refresh dashboard |
| 401 Unauthorized | Double-check API key is correct |

---

## 📚 Full Documentation

See **[ARIZE_TRACING_SETUP.md](./ARIZE_TRACING_SETUP.md)** for:
- Detailed configuration options
- Data privacy information
- Advanced debugging techniques
- Analytics setup

---

**Need help?** [Arize Docs](https://arize.com/docs) | [Support](mailto:support@arize.com)

