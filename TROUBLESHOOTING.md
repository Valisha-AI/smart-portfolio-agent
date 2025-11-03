# 🔧 Troubleshooting Guide - Smart Portfolio Agent

## ✅ ISSUE RESOLVED: "Not Fetching Data"

### Problem
The Smart Portfolio Agent was not fetching data from Yahoo Finance.

### Root Cause
**Dependencies were not installed** in the virtual environment.

### Solution Applied ✅
1. Fixed package name: `openinference-semconv` → `openinference-semantic-conventions`
2. Installed all dependencies: `pip install -r backend/requirements.txt`
3. Verified data fetching works: Yahoo Finance API is operational
4. Tested portfolio generation: **Working perfectly!**

---

## 🎯 Quick Diagnostics Checklist

If the agent stops working, run through this checklist:

### 1️⃣ Check Virtual Environment
```bash
cd /Users/valishagravesnew/Cursor/smart-portfolio-agent
source .venv/bin/activate
python -c "import yfinance; print('✅ yfinance installed')"
```

**Expected**: `✅ yfinance installed`  
**If error**: Run `pip install -r backend/requirements.txt`

### 2️⃣ Check Environment Variables
```bash
cat backend/.env | grep OPENAI_API_KEY
```

**Expected**: Should show your OpenAI API key  
**If missing**: Create `.env` file in `backend/` directory

### 3️⃣ Test Data Fetching
```bash
python -c "import yfinance as yf; ticker = yf.Ticker('AAPL'); print(ticker.info.get('longName', 'Error'))"
```

**Expected**: `Apple Inc.`  
**If error**: Yahoo Finance API might be down (temporary)

### 4️⃣ Check Server Health
```bash
# Start server
cd backend
python main.py &

# Wait 5 seconds, then check
curl http://localhost:8000/health
```

**Expected**: 
```json
{
  "status": "healthy",
  "checks": {
    "api": "ok",
    "llm": "ok"
  }
}
```

### 5️⃣ Test Portfolio Generation
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

**Expected**: JSON response with allocation array  
**If error**: Check logs in terminal where server is running

---

## 🐛 Common Issues & Fixes

### Issue 1: ModuleNotFoundError: No module named 'yfinance'

**Symptoms:**
```
ModuleNotFoundError: No module named 'yfinance'
```

**Fix:**
```bash
cd /Users/valishagravesnew/Cursor/smart-portfolio-agent
source .venv/bin/activate
pip install -r backend/requirements.txt
```

---

### Issue 2: OpenAI API Key Missing

**Symptoms:**
```
Error: OpenAI API key not found
```

**Fix:**
Create `backend/.env` file:
```bash
cd backend
cat > .env << 'EOF'
OPENAI_API_KEY=sk-your-key-here
ENVIRONMENT=development
DEBUG=true
EOF
```

---

### Issue 3: Yahoo Finance Rate Limiting

**Symptoms:**
```
HTTPError: 429 Too Many Requests
```

**Fix:**
- Wait 1-2 minutes before retrying
- Yahoo Finance has rate limits (2,000 requests/hour per IP)
- If persistent, implement caching (Redis)

---

### Issue 4: Empty/Null Data Returned

**Symptoms:**
```json
{
  "company_name": "AAPL",
  "sector": "Unknown",
  "market_cap": 0
}
```

**Possible Causes:**
1. **Invalid ticker** - Verify ticker exists on Yahoo Finance
2. **Delisted stock** - Company no longer traded
3. **API changes** - Yahoo Finance changed data format

**Fix:**
```bash
# Test with known good ticker
python -c "
import yfinance as yf
ticker = yf.Ticker('AAPL')
print(ticker.info)
"
```

If AAPL works but your ticker doesn't, the ticker might be invalid.

---

### Issue 5: Server Won't Start

**Symptoms:**
```
Address already in use: 8000
```

**Fix:**
```bash
# Kill existing server
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --port 8001
```

---

### Issue 6: Slow Response Times

**Symptoms:**
- Portfolio generation takes > 30 seconds
- Timeout errors

**Possible Causes:**
1. Yahoo Finance API is slow
2. Too many peer companies being fetched
3. LLM rationale generation is slow

**Fix:**
1. Reduce `max_holdings` in request (try 3 instead of 5)
2. Set `include_etfs: false` to skip ETF lookups
3. Check OpenAI API status

---

### Issue 7: Import Errors

**Symptoms:**
```
ImportError: cannot import name 'ChatOpenAI' from 'langchain_openai'
```

**Fix:**
```bash
# Reinstall langchain packages
pip uninstall langchain langchain-openai langchain-core -y
pip install langchain>=0.3.7 langchain-openai>=0.2.10 langchain-core>=0.3.15
```

---

### Issue 8: Arize Tracing Not Working

**Symptoms:**
```
🔍 Arize Tracing: ⚠️  Not configured
```

**This is OK!** Tracing is optional. To enable:

1. Sign up at [app.arize.com](https://app.arize.com)
2. Get your Space ID and API Key
3. Add to `backend/.env`:
```bash
ARIZE_SPACE_ID=your-space-id
ARIZE_API_KEY=your-api-key
ARIZE_PROJECT_NAME=smart-portfolio-agent
```
4. Restart server

---

## 🔍 Debug Mode

Enable detailed logging:

```bash
# In backend/.env
DEBUG=true
LOG_LEVEL=DEBUG
```

Then check logs:
```bash
cd backend
python main.py 2>&1 | tee debug.log
```

---

## 📊 Verify Everything Works

**Test Script:**
```bash
#!/bin/bash

echo "🔍 Smart Portfolio Agent - Health Check"
echo "========================================"

# 1. Check virtual environment
echo "1. Checking virtual environment..."
source .venv/bin/activate
python -c "import yfinance, langchain, fastapi" && echo "✅ Dependencies OK" || echo "❌ Dependencies missing"

# 2. Check environment variables
echo -e "\n2. Checking environment variables..."
[ -f backend/.env ] && echo "✅ .env file exists" || echo "❌ .env file missing"

# 3. Test data fetch
echo -e "\n3. Testing Yahoo Finance..."
python -c "import yfinance as yf; yf.Ticker('AAPL').info['longName']" && echo "✅ Yahoo Finance OK" || echo "❌ Yahoo Finance error"

# 4. Start server
echo -e "\n4. Starting server..."
cd backend
python main.py > /dev/null 2>&1 &
SERVER_PID=$!
sleep 5

# 5. Test health endpoint
echo -e "\n5. Testing health endpoint..."
curl -s http://localhost:8000/health | grep -q '"status": "healthy"' && echo "✅ Server healthy" || echo "❌ Server error"

# 6. Test portfolio generation
echo -e "\n6. Testing portfolio generation..."
RESULT=$(curl -s -X POST http://localhost:8000/api/v1/portfolio/generate \
  -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","investment_amount":10000,"risk_level":"medium","include_etfs":true,"max_holdings":5}')
echo "$RESULT" | grep -q '"ticker": "AAPL"' && echo "✅ Portfolio generation OK" || echo "❌ Portfolio generation error"

# Cleanup
kill $SERVER_PID 2>/dev/null

echo -e "\n========================================"
echo "✅ All checks complete!"
```

Save as `health_check.sh`, make executable, and run:
```bash
chmod +x health_check.sh
./health_check.sh
```

---

## 📞 Still Having Issues?

### Collected Information Needed:
1. **Error message** (full traceback)
2. **Python version**: `python --version`
3. **OS**: `uname -a`
4. **Dependencies**: `pip list | grep -E "yfinance|langchain|fastapi"`
5. **Server logs** (last 50 lines)

### Where to Get Help:
- **GitHub Issues**: (if public repo)
- **Documentation**: See `ARIZE_TRACING_SETUP.md`, `README.md`
- **Arize Support**: support@arize.com (for tracing issues)

---

## 🎉 Success Indicators

Your agent is working if you see:

✅ **Server Logs:**
```
🚀 Smart Portfolio API starting up...
🔑 OpenAI API Key: ✅ Configured
✅ Portfolio generated successfully!
```

✅ **Health Endpoint:**
```json
{"status": "healthy", "checks": {"api": "ok", "llm": "ok"}}
```

✅ **Portfolio Response:**
```json
{
  "allocation": [
    {"ticker": "AAPL", "allocation_percent": 35, ...},
    ...
  ],
  "summary": {
    "average_earnings_quality": 4.2,
    ...
  }
}
```

---

**Last Updated**: November 3, 2025  
**Status**: All systems operational ✅

