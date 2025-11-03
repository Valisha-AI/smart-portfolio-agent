# Arize Tracing Setup Guide

This guide will help you set up Arize tracing for the Smart Portfolio Agent to monitor your LLM application performance, debug issues, and track costs.

## 📋 What is Arize?

[Arize](https://arize.com) is an observability platform for AI/LLM applications that provides:
- **Tracing**: End-to-end visibility into your LangGraph agent workflows
- **Monitoring**: Track latency, errors, token usage, and costs
- **Debugging**: Inspect individual traces to troubleshoot issues
- **Analytics**: Understand user behavior and model performance

## 🚀 Quick Setup (5 minutes)

### Step 1: Get Your Arize Credentials

1. Sign up for a free Arize account at [https://app.arize.com](https://app.arize.com)
2. Navigate to **Settings** → **API Keys**
3. Copy your:
   - **Space ID** (looks like: `abc123def456`)
   - **API Key** (looks like: `sk_abc123...`)

### Step 2: Install Dependencies

```bash
cd /Users/valishagravesnew/Cursor/smart-portfolio-agent/backend
pip install -r requirements.txt
```

This will install:
- `arize-otel` - Arize's OpenTelemetry integration
- `openinference-instrumentation-langchain` - Auto-instrumentation for LangChain/LangGraph
- `openinference-instrumentation-openai` - Auto-instrumentation for OpenAI
- OpenTelemetry SDK packages

### Step 3: Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
cd backend
touch .env
```

Add your Arize credentials to `.env`:

```bash
# OpenAI API Key (Required)
OPENAI_API_KEY=sk-your-openai-key-here

# Arize Tracing Configuration (Required for Observability)
ARIZE_SPACE_ID=your-arize-space-id-here
ARIZE_API_KEY=your-arize-api-key-here
ARIZE_PROJECT_NAME=smart-portfolio-agent

# Optional: CapitalCube API
CAPITALCUBE_API_KEY=your-capitalcube-key-here

# Optional: Redis Cache
REDIS_URL=redis://localhost:6379

# Environment
ENVIRONMENT=development
```

**Important**: Replace `your-arize-space-id-here` and `your-arize-api-key-here` with your actual credentials from Step 1.

### Step 4: Start the Server

```bash
cd backend
python main.py
```

You should see:
```
🚀 Smart Portfolio API starting up...
📊 Version: 1.0.0
🔑 OpenAI API Key: ✅ Configured
🔍 Arize Tracing: ✅ Enabled (Project: smart-portfolio-agent)
Ready to accept requests!
```

### Step 5: Generate a Portfolio (Test Tracing)

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

### Step 6: View Traces in Arize

1. Go to [https://app.arize.com](https://app.arize.com)
2. Select your **Space**
3. Navigate to **Tracing** in the left sidebar
4. You should see traces for your portfolio generation requests!

---

## 🔍 What Gets Traced?

The Smart Portfolio Agent automatically traces:

### 1. **LangChain/LangGraph Operations**
   - Agent invocations
   - Tool calls (Yahoo Finance, scoring algorithms)
   - State transitions
   - Chain execution

### 2. **OpenAI API Calls**
   - Model used (e.g., `gpt-4o-mini`)
   - Prompts sent
   - Responses received
   - Token usage and costs
   - Latency

### 3. **Custom Attributes**
   - Request parameters (ticker, amount, risk level)
   - Portfolio allocation results
   - Quality scores
   - Errors and exceptions

---

## 🎯 Key Features

### Trace Details
Each trace shows:
- **Request Flow**: See the entire agent workflow from input to output
- **Timing**: Understand where time is spent
- **Token Usage**: Track OpenAI costs per request
- **Errors**: Debug failures with full stack traces

### Dashboard & Analytics
- **Performance Metrics**: Average latency, P95, P99
- **Cost Tracking**: Daily/weekly spend on OpenAI
- **Error Rates**: Monitor failures over time
- **User Sessions**: Track user behavior patterns

### Debugging
- **Inspect Prompts**: See exactly what was sent to GPT-4
- **View Responses**: Check LLM outputs
- **Tool Execution**: Verify data fetched from Yahoo Finance
- **State Evolution**: Track how agent state changes

---

## 🛠️ Configuration Options

### Change Project Name
Update your `.env` file:
```bash
ARIZE_PROJECT_NAME=my-custom-name
```

### Multiple Environments
Use different project names for dev/staging/prod:
```bash
# Development
ARIZE_PROJECT_NAME=smart-portfolio-dev

# Production
ARIZE_PROJECT_NAME=smart-portfolio-prod
```

---

## 🔒 Data Privacy

Arize uses **Azure OpenAI** infrastructure with strict privacy guarantees:
- ✅ Your data is **NOT** used to train models
- ✅ Your data is **NOT** shared with third parties
- ✅ Microsoft-controlled infrastructure
- ✅ SOC 2 Type II certified

See [Arize's data privacy docs](https://arize.com/docs/ax/arize-copilot#data-privacy) for more details.

---

## 🧪 Verify Tracing Works

### Check Health Endpoint
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "checks": {
    "api": "ok",
    "llm": "ok",
    "cache": "not_configured",
    "tracing": "ok"
  },
  "tracing": {
    "enabled": true,
    "space_id_configured": true,
    "api_key_configured": true,
    "project_name": "smart-portfolio-agent"
  }
}
```

### Check Server Logs
Look for this message on startup:
```
✅ Arize tracing initialized successfully for project: smart-portfolio-agent
🔍 Traces will be available at: https://app.arize.com/organizations/YOUR_ORG/spaces/YOUR_SPACE
```

---

## ❌ Troubleshooting

### "Arize Tracing: ⚠️ Not configured"
**Solution**: Ensure `ARIZE_SPACE_ID` and `ARIZE_API_KEY` are set in your `.env` file.

### "Failed to import Arize tracing libraries"
**Solution**: Run `pip install -r backend/requirements.txt`

### "Traces not appearing in Arize"
**Checklist**:
1. ✅ Verify credentials are correct
2. ✅ Check internet connectivity
3. ✅ Wait 1-2 minutes for traces to appear
4. ✅ Refresh the Arize dashboard

### "401 Unauthorized" in logs
**Solution**: Your API key is invalid. Double-check it matches the one in Arize settings.

---

## 📚 Additional Resources

- **Arize Documentation**: https://arize.com/docs
- **LangGraph Tracing**: https://arize.com/docs/ax/tracing-integrations
- **OpenInference Spec**: https://github.com/Arize-ai/openinference
- **Support**: support@arize.com or [Slack community](https://arize.com/slack)

---

## 🎉 Next Steps

Now that tracing is set up:

1. **Generate some portfolios** to collect trace data
2. **Explore the Arize dashboard** to understand your agent's behavior
3. **Set up monitors** to get alerts for errors or latency spikes
4. **Optimize prompts** based on trace insights
5. **Track costs** to stay within budget

Happy tracing! 🚀

