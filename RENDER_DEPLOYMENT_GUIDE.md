# 🚀 Render Deployment Guide - Smart Portfolio Agent

## 🔴 Current Issue: "Error: Failed to fetch"

Your app at `smart-portfolio-agent.onrender.com` is showing "Error: Failed to fetch". This typically means:

1. **Service is down** - Free tier services sleep after 15 min of inactivity
2. **Build failed** - Dependencies didn't install correctly
3. **Missing environment variables** - API keys not configured
4. **Port binding issue** - Server not listening on correct port

---

## 🔧 Quick Fixes

### Fix 1: Check Render Dashboard

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Find your `smart-portfolio-agent` service
3. Check the **Logs** tab for errors
4. Look for recent deployments in **Events** tab

### Fix 2: Wake Up Sleeping Service

Free tier services sleep after 15 minutes of inactivity:

```bash
# Wake it up by visiting
curl https://smart-portfolio-agent.onrender.com/health
```

**Wait 30-60 seconds** for the service to wake up, then try again.

### Fix 3: Check Environment Variables

In Render Dashboard → Your Service → Environment:

**Required:**
```
OPENAI_API_KEY=sk-your-key-here
```

**Optional but recommended:**
```
ARIZE_SPACE_ID=your-space-id
ARIZE_API_KEY=your-api-key
ARIZE_PROJECT_NAME=smart-portfolio-agent
```

### Fix 4: Trigger Manual Deploy

In Render Dashboard:
1. Go to your service
2. Click **Manual Deploy** → **Deploy latest commit**
3. Wait 5-10 minutes for build to complete
4. Check logs for errors

---

## 📋 Complete Deployment Checklist

### Step 1: Verify Render Configuration

Your `render.yaml` should look like this:

```yaml
services:
  - type: web
    name: smart-portfolio-agent
    env: python
    region: oregon
    plan: free
    buildCommand: "pip install -r backend/requirements.txt"
    startCommand: "cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: OPENAI_API_KEY
        sync: false
```

✅ This looks correct!

### Step 2: Verify Procfile (Backup)

Your `Procfile`:
```
web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

✅ This looks correct!

### Step 3: Verify Runtime

Your `runtime.txt`:
```
python-3.11.0
```

✅ This looks correct!

### Step 4: Verify Requirements

Check that `backend/requirements.txt` has all dependencies:
- ✅ fastapi
- ✅ uvicorn
- ✅ yfinance
- ✅ langchain packages
- ✅ All other dependencies

---

## 🐛 Common Render Deployment Errors

### Error 1: Build Timeout

**Symptoms:** Build takes > 15 minutes and times out

**Fix:** Simplify `requirements.txt` or upgrade to paid tier

### Error 2: Module Not Found

**Symptoms:** `ModuleNotFoundError: No module named 'yfinance'`

**Fix:** 
1. Check `buildCommand` points to correct requirements file
2. Verify all packages are in `backend/requirements.txt`

### Error 3: Port Binding Failed

**Symptoms:** Service starts but can't be accessed

**Fix:** Ensure using `$PORT` environment variable:
```python
# In main.py (already correct)
uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
```

### Error 4: Health Check Fails

**Symptoms:** Service marked as unhealthy

**Fix:** Add health check configuration in Render:
- Path: `/health`
- Expected status: 200

---

## 🔍 Debugging Steps

### 1. Check Render Logs

In Render Dashboard → Your Service → Logs, look for:

**Good startup:**
```
🚀 Smart Portfolio API starting up...
🔑 OpenAI API Key: ✅ Configured
Ready to accept requests!
INFO:     Uvicorn running on http://0.0.0.0:PORT
```

**Bad startup:**
```
ModuleNotFoundError: No module named 'X'
ERROR: Could not find a version that satisfies...
Address already in use
```

### 2. Test Deployment Locally

Simulate Render environment:

```bash
# Set PORT variable like Render does
cd /Users/valishagravesnew/Cursor/smart-portfolio-agent
export PORT=10000
cd backend
python -c "import os; print(os.getenv('PORT'))"  # Should print 10000
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 3. Test Deployed Service

```bash
# Health check
curl https://smart-portfolio-agent.onrender.com/health

# Full test
curl -X POST https://smart-portfolio-agent.onrender.com/api/v1/portfolio/generate \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "investment_amount": 10000,
    "risk_level": "medium",
    "include_etfs": true,
    "max_holdings": 5
  }'
```

---

## 🚀 Deployment from Scratch

If starting fresh on Render:

### 1. Push Code to GitHub

```bash
cd /Users/valishagravesnew/Cursor/smart-portfolio-agent
git add .
git commit -m "Fix: Add investment_amount parameter to LLM function"
git push origin main
```

### 2. Create New Web Service on Render

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Connect your GitHub repo
4. Configure:
   - **Name**: `smart-portfolio-agent`
   - **Region**: Oregon (closest to you)
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

### 3. Add Environment Variables

Click **Add Environment Variable**:

```
OPENAI_API_KEY = sk-your-actual-key-here
```

Optional:
```
ARIZE_SPACE_ID = your-space-id
ARIZE_API_KEY = your-api-key
ENVIRONMENT = production
```

### 4. Deploy

Click **Create Web Service**

Wait 5-10 minutes for first deploy. Watch logs for issues.

---

## 📊 Verify Deployment Works

### Check 1: Service Status

In Render Dashboard:
- Status should be **Live** (green dot)
- Not **Suspended** or **Build Failed**

### Check 2: Health Endpoint

```bash
curl https://smart-portfolio-agent.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "checks": {
    "api": "ok",
    "llm": "ok"
  }
}
```

### Check 3: Generate Portfolio

```bash
curl -X POST https://smart-portfolio-agent.onrender.com/api/v1/portfolio/generate \
  -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","investment_amount":10000,"risk_level":"medium","include_etfs":true,"max_holdings":5}'
```

Should return portfolio JSON (wait 30-60 seconds first time).

---

## ⚡ Free Tier Limitations

### What to Expect:

1. **Cold Starts**: Service sleeps after 15 min inactivity
   - First request after sleep takes 30-60 seconds
   - Subsequent requests are fast

2. **Limited Resources**: 
   - 512 MB RAM
   - Shared CPU
   - May be slow under load

3. **750 Hours/Month**: Free for 1 service

### Upgrade to Paid if Needed:

If you need:
- No cold starts
- More RAM/CPU
- Custom domain
- 99.9% uptime

→ Upgrade to Starter ($7/month)

---

## 🔄 Update Deployed Code

When you fix bugs locally:

```bash
# 1. Test locally first
cd /Users/valishagravesnew/Cursor/smart-portfolio-agent/backend
python main.py
# Test with curl...

# 2. Commit and push
git add .
git commit -m "Fix: your-fix-description"
git push origin main

# 3. Render auto-deploys (if enabled)
# Or manually trigger in dashboard
```

Render will automatically rebuild and redeploy.

---

## 📞 Still Having Issues?

### Collect This Information:

1. **Render Logs** (last 100 lines)
2. **Service URL**: smart-portfolio-agent.onrender.com
3. **Error message** from browser/curl
4. **Environment variables** (redact API keys)

### Get Help:

- **Render Support**: [render.com/support](https://render.com/support)
- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Community**: [community.render.com](https://community.render.com)

---

## ✅ Next Steps for You

1. **Go to Render Dashboard** → Check logs for errors
2. **Add OPENAI_API_KEY** if missing in environment variables
3. **Trigger manual deploy** to use the fixed code
4. **Wait 5-10 minutes** for build to complete
5. **Test** the health endpoint
6. **Monitor logs** for any errors

The "Failed to fetch" error should resolve once:
- ✅ Code bug is fixed (done!)
- ✅ Service is deployed with correct environment variables
- ✅ Service is awake and running

---

**Need immediate help?** Share the Render logs and I can diagnose further!

