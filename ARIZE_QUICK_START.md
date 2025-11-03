# 🔍 Arize AX - Quick Start

## ✅ **Arize AX Observability is NOW Configured!**

Your Smart Portfolio Agent is **ready for full observability** in Arize AX. Just add credentials and go!

---

## ⚡ 2-Minute Setup

### **1. Get Credentials**
- Go to: **[app.arize.com](https://app.arize.com/settings/api-keys)**
- Copy your **Space ID** and **API Key**

### **2. Add to Environment**

**Local Development (`backend/.env`):**
```bash
ARIZE_SPACE_ID=your-space-id
ARIZE_API_KEY=your-api-key
ARIZE_PROJECT_NAME=smart-portfolio-agent
```

**Render (Production):**
1. Dashboard → smart-portfolio-agent → Environment
2. Add:
   - `ARIZE_SPACE_ID` = your-space-id
   - `ARIZE_API_KEY` = your-api-key
   - `ARIZE_PROJECT_NAME` = smart-portfolio-agent
3. Save → Redeploy

### **3. Restart & Test**

```bash
# Local
cd backend
python main.py
# Look for: ✅ Arize AX tracing enabled

# Generate a request
curl -X POST http://localhost:8000/api/v1/portfolio/generate \
  -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","investment_amount":10000,"risk_level":"medium","include_etfs":true,"max_holdings":5}'
```

### **4. View in Arize**
- Go to: **[app.arize.com](https://app.arize.com)**
- Click **Tracing** → **smart-portfolio-agent**
- See your traces! 🎉

---

## 📊 What You Get

### **Full Agent Visibility**
```
Portfolio Generation (AAPL, $10k, medium)
├─ get_stock_info(AAPL) - 1.2s
├─ find_sector_peers(Technology) - 1.3s  
├─ calculate_scores(5 companies) - 3.3s
├─ allocate_medium_risk - 0.3s
└─ generate_llm_rationale
   ├─ Model: gpt-4o-mini
   ├─ Tokens: 523 in, 187 out
   ├─ Cost: $0.0023
   └─ Latency: 2.3s ✅
```

### **Automatic Tracking**
✅ LangGraph agent workflows  
✅ Tool executions (Yahoo Finance, scoring)  
✅ OpenAI API calls (prompts, responses, tokens, costs)  
✅ Error traces and debugging info  
✅ Performance metrics (latency, throughput)

---

## 🎯 Use Cases

### **1. Debugging**
- Find why a request failed
- See exact LLM prompts that caused issues
- Identify slow operations

### **2. Optimization**
- Reduce token usage to cut costs
- Identify bottlenecks in agent workflow
- Improve response times

### **3. Monitoring**
- Track daily OpenAI spending
- Alert on error rate spikes
- Monitor P95 latency trends

### **4. Analysis**
- Which tickers are most requested?
- What risk levels do users prefer?
- Are LLM rationales high quality?

---

## 🔧 Already Configured

✅ **Dependencies installed** - `arize-otel`, instrumentors  
✅ **Tracing module** - `backend/config/tracing.py`  
✅ **Auto-instrumentation** - LangChain + OpenAI  
✅ **FastAPI integration** - Runs on startup  
✅ **Health endpoint** - Shows tracing status

**You just need to add the environment variables!**

---

## 📚 Documentation

- **Quick Setup**: This file
- **Detailed Guide**: [ARIZE_AX_SETUP.md](ARIZE_AX_SETUP.md)
- **Arize Docs**: https://arize.com/docs/ax/tracing-integrations

---

## ✅ Verification

After adding credentials:

```bash
# Check health endpoint
curl http://localhost:8000/health | python3 -m json.tool | grep tracing

# Should see:
# "tracing": "ok"
# "enabled": true
```

**Server logs should show:**
```
✅ Arize AX tracing enabled: smart-portfolio-agent
🔍 View traces at: https://app.arize.com
```

---

## 💡 Tips

1. **Start with dev project**: `ARIZE_PROJECT_NAME=portfolio-dev`
2. **Generate test data**: Make 5-10 requests with different tickers
3. **Explore Arize**: Look at traces, timeline views, metrics
4. **Set up alerts**: Monitor errors and latency
5. **Optimize**: Use insights to reduce costs and improve performance

---

## 🎉 That's It!

Your agent is fully instrumented for Arize AX observability. Just add those two environment variables and you're live!

**Questions?** See [ARIZE_AX_SETUP.md](ARIZE_AX_SETUP.md) for detailed info.

