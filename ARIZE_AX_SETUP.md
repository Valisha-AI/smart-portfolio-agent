# 🔍 Arize AX Observability Setup Guide

## Overview

This guide shows you how to enable **Arize AX** observability for your Smart Portfolio Agent, giving you full visibility into your LangGraph agent workflows.

---

## ✅ What You'll Get

Once configured, you'll see in **Arize AX**:

### 📊 **Agent Workflow Visualization**
- Complete trace of portfolio generation flow
- Visual graph of agent execution path
- Node-by-node timing breakdown

### 🔍 **Detailed Trace Information**
```
Portfolio Generation Request (AAPL, $10k, medium risk)
├─ 📊 Fetch Stock Data (AAPL)
│  └─ Yahoo Finance API: 1.2s, 200 OK
├─ 🔎 Find Peer Companies  
│  └─ Sector lookup: Technology → [MSFT, GOOGL, NVDA, META]
├─ 💯 Score Companies
│  ├─ Calculate scores for 5 tickers
│  └─ Average score: 4.2/5
├─ 💰 Apply Allocation Algorithm
│  └─ Medium risk: quality-weighted distribution
└─ 🤖 Generate LLM Rationale
   ├─ Model: gpt-4o-mini
   ├─ Tokens: 523 input, 187 output
   ├─ Cost: $0.0023
   ├─ Latency: 2.3s
   └─ Prompt + Response captured
```

### 📈 **Performance Metrics**
- Average request latency
- OpenAI token usage per request
- Cost tracking (spend per day/week)
- Error rates and failure analysis
- P50/P95/P99 percentiles

### 🐛 **Debugging**
- Full error stack traces
- Failed requests with input/output
- Slow trace identification
- Prompt/response inspection

---

## 🚀 Quick Setup (5 Minutes)

### **Step 1: Get Arize AX Credentials**

1. Sign up at **[app.arize.com](https://app.arize.com)** (free tier available)
2. Go to **Settings** → **API Keys**
3. Copy your:
   - **Space ID** (looks like: `abc123`)
   - **API Key** (looks like: `sk_abc123...`)

### **Step 2: Configure Environment Variables**

Add to your `.env` file:

```bash
# Arize AX Observability
ARIZE_SPACE_ID=your-space-id-here
ARIZE_API_KEY=your-api-key-here
ARIZE_PROJECT_NAME=smart-portfolio-agent
```

**For Render (Production):**
1. Go to Render Dashboard → Your Service
2. Click **Environment**
3. Add these environment variables:
   - `ARIZE_SPACE_ID` = your space ID
   - `ARIZE_API_KEY` = your API key
   - `ARIZE_PROJECT_NAME` = smart-portfolio-agent

### **Step 3: Restart Your Application**

**Local:**
```bash
cd backend
source ../.venv/bin/activate
python main.py
```

Look for: `✅ Arize AX tracing enabled: smart-portfolio-agent`

**Render:**
- Click **Manual Deploy** → **Deploy latest commit**
- Wait for deployment
- Check logs for `✅ Arize AX tracing enabled`

### **Step 4: Generate Some Requests**

```bash
# Generate a portfolio to create traces
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

### **Step 5: View in Arize AX**

1. Go to **[app.arize.com](https://app.arize.com)**
2. Select your **Space**
3. Click **Tracing** in the left sidebar
4. Select project: **smart-portfolio-agent**
5. You should see your traces! 🎉

---

## 📊 What You'll See in Arize AX

### **1. Tracing Dashboard**

Main view showing:
- **Total traces** (number of portfolio generations)
- **Average latency** (end-to-end response time)
- **Error rate** (percentage of failed requests)
- **Cost** (OpenAI API spending)

### **2. Individual Trace View**

Click any trace to see:

**Timeline View:**
```
│ 
├─ [0.0s - 1.2s] get_stock_info(AAPL)
│  └─ Inputs: ticker="AAPL"
│  └─ Outputs: {company_name, sector, market_cap...}
│
├─ [1.2s - 2.5s] find_sector_peers(Technology)
│  └─ Inputs: sector="Technology", limit=8
│  └─ Outputs: [MSFT, GOOGL, NVDA, META, AMD]
│
├─ [2.5s - 5.8s] calculate_fundamental_score (5 companies)
│  └─ Parallel execution
│
├─ [5.8s - 6.1s] allocate_medium_risk
│  └─ Inputs: scored_peers, etf=XLK
│  └─ Outputs: allocation percentages
│
└─ [6.1s - 8.4s] 🔥 OpenAI LLM Call
   ├─ Model: gpt-4o-mini
   ├─ Temperature: 0.7
   ├─ Input tokens: 523
   ├─ Output tokens: 187
   ├─ Cost: $0.0023
   ├─ Latency: 2.3s
   ├─ Prompt: "You are a financial analyst..."
   └─ Response: "This balanced quality-weighted portfolio..."
```

**Attributes Tab:**
- Request parameters (ticker, amount, risk_level)
- Model information
- Token counts
- Error details (if any)

**Metadata Tab:**
- Session ID
- User ID (if set)
- Custom tags
- Environment info

### **3. Analytics**

**Performance Metrics:**
- Latency distribution (histogram)
- Requests per hour/day
- Token usage trends
- Cost over time

**Quality Metrics:**
- Error types and frequency
- Slow requests (> threshold)
- Failed tool calls
- LLM refusals or errors

---

## 🎯 What Gets Traced

### **Automatic Instrumentation:**

Because you're using **LangGraph** and **OpenAI**, Arize automatically captures:

✅ **Agent Workflow**
- Complete execution graph
- Node transitions
- State changes
- Conditional logic

✅ **Tool Executions**
- `get_stock_info()` calls
- `find_sector_peers()` lookups
- `calculate_fundamental_score()` operations
- Yahoo Finance API calls

✅ **LLM Calls**
- Model name and version
- Full prompts (with context)
- Complete responses
- Token usage (input/output)
- Cost per request
- Latency metrics

✅ **Error Handling**
- Exception traces
- Failed operations
- Retry attempts
- Fallback logic

### **Request Context:**

Each trace includes:
```python
{
  "input": {
    "ticker": "AAPL",
    "investment_amount": 10000,
    "risk_level": "medium",
    "include_etfs": true,
    "max_holdings": 5
  },
  "output": {
    "allocation": [...],
    "summary": {...},
    "rationale": "..."
  },
  "metadata": {
    "timestamp": "2025-11-03T18:30:00Z",
    "latency_ms": 8400,
    "tokens_used": 710,
    "cost_usd": 0.0023
  }
}
```

---

## 🔬 Advanced Features

### **Session Tracking**

Track user sessions across multiple requests:

```python
# In your API endpoint (main.py)
from openinference.instrumentation import using_attributes

@app.post("/api/v1/portfolio/generate")
async def generate_portfolio(req: PortfolioRequest):
    # Set session/user context for tracing
    with using_attributes(
        session_id=req.session_id,  # if you track sessions
        user_id=req.user_id,        # if you track users
    ):
        result = generate_portfolio_allocation(...)
        return result
```

### **Custom Attributes**

Add custom metadata to traces:

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)
span = trace.get_current_span()

# Add custom attributes
span.set_attribute("portfolio.ticker", ticker)
span.set_attribute("portfolio.risk_level", risk_level)
span.set_attribute("portfolio.total_holdings", len(allocation))
```

### **Error Tracking**

Errors are automatically captured, but you can add context:

```python
try:
    result = some_operation()
except Exception as e:
    span = trace.get_current_span()
    span.record_exception(e)
    span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
    raise
```

---

## 📈 Monitoring & Alerts

### **Set Up Monitors**

In Arize AX:
1. Go to **Monitors**
2. Create new monitor
3. Set conditions:
   - Alert if error rate > 5%
   - Alert if latency P95 > 10s
   - Alert if daily cost > $5
4. Configure notifications (email, Slack, etc.)

### **Performance Thresholds**

**Good Performance:**
- Latency P50 < 3s
- Latency P95 < 10s
- Error rate < 1%
- Cost per request < $0.01

**Needs Optimization:**
- Latency P95 > 15s
- Error rate > 5%
- Cost per request > $0.05

---

## 🐛 Debugging with Arize AX

### **Find Slow Requests**

1. Go to **Tracing** → **Filters**
2. Set: `latency > 10s`
3. Sort by latency descending
4. Click on slowest trace
5. Identify bottleneck in timeline view

**Common Bottlenecks:**
- Yahoo Finance API slow response
- Too many peer companies being scored
- LLM generation timeout

### **Debug Failed Requests**

1. Filter: `status = error`
2. Click on failed trace
3. Check **Error** tab for:
   - Exception type
   - Stack trace
   - Failed operation
4. Check **Attributes** for request context

**Common Errors:**
- Invalid ticker symbol
- OpenAI rate limit
- Yahoo Finance timeout
- JSON parsing failure in LLM response

### **Analyze LLM Behavior**

1. Find traces with LLM calls
2. Click to expand LLM span
3. Review:
   - **Prompt quality**: Is context sufficient?
   - **Response quality**: Is output formatted correctly?
   - **Token usage**: Are you over-prompting?
   - **Latency**: Is response time acceptable?

**Optimization Tips:**
- Reduce prompt length if tokens > 1000
- Use cheaper model (gpt-4o-mini vs gpt-4) if appropriate
- Add response format constraints
- Implement caching for repeated queries

---

## 💰 Cost Tracking

### **OpenAI Cost Breakdown**

Arize automatically calculates costs based on:
- Model used (gpt-4o-mini, gpt-4, etc.)
- Input tokens
- Output tokens
- Pricing tier

**View in Arize:**
- **Tracing** → **Cost Analysis**
- See cost per request
- Daily/weekly/monthly totals
- Cost by model
- Most expensive requests

### **Optimize Costs**

**Strategies:**
1. **Cache results**: Store portfolio for same ticker/params
2. **Reduce token usage**: Shorten prompts
3. **Use cheaper models**: gpt-4o-mini for rationale generation
4. **Batch requests**: If possible
5. **Set budget alerts**: Get notified before overspending

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Arize credentials added to `.env` (or Render environment)
- [ ] Server starts with `✅ Arize AX tracing enabled` message
- [ ] Health endpoint shows `"tracing": {"enabled": true}`
- [ ] Generate test portfolio request
- [ ] Wait 1-2 minutes for traces to appear
- [ ] Check Arize AX dashboard - see traces
- [ ] Click on a trace - see full timeline
- [ ] Verify LLM calls are captured with tokens/cost
- [ ] Check that prompts and responses are visible

---

## 🎓 Best Practices

### **1. Use Descriptive Project Names**
```bash
# Development
ARIZE_PROJECT_NAME=smart-portfolio-dev

# Staging
ARIZE_PROJECT_NAME=smart-portfolio-staging

# Production
ARIZE_PROJECT_NAME=smart-portfolio-prod
```

### **2. Add Request Context**
```python
span.set_attribute("request.ticker", ticker)
span.set_attribute("request.risk_level", risk_level)
span.set_attribute("request.amount_usd", amount)
```

### **3. Monitor Key Metrics**
- Daily active requests
- Average latency
- Error rate trends
- Cost per day

### **4. Regular Reviews**
- Weekly: Check error spikes
- Monthly: Review cost trends
- Quarterly: Optimize slow operations

---

## 📞 Support

**Arize Support:**
- Email: support@arize.com
- Docs: https://arize.com/docs
- Slack: [Arize Community](https://arize.com/slack)

**Common Issues:**
- **Traces not appearing**: Wait 2-3 minutes, check credentials
- **High costs**: Review token usage, implement caching
- **Slow traces**: Identify bottleneck in timeline view
- **Missing data**: Verify instrumentors are loaded

---

## 🎉 You're All Set!

Once configured, **every portfolio request** will be automatically traced in Arize AX, giving you complete visibility into your agent's behavior.

**Next Steps:**
1. Generate some test requests
2. Explore the Arize AX dashboard
3. Set up monitors for critical metrics
4. Use insights to optimize performance

---

**Happy Observing!** 🔍✨

