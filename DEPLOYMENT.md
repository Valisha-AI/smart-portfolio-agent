# 🚀 Deployment Guide - Render

This guide walks you through deploying the Smart Portfolio Agent to Render.

## Prerequisites

- GitHub account with the repository pushed
- OpenAI API key
- Render account (sign up at https://render.com)

## Step-by-Step Deployment

### 1. Sign Up / Log In to Render

Go to: https://render.com
- Click "Get Started for Free"
- Sign up with your GitHub account

### 2. Create New Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub account if not already connected
3. Find and select `Valisha-AI/smart-portfolio-agent`
4. Click "Connect"

### 3. Configure Your Service

Fill in these settings:

**Basic Settings:**
- **Name:** `smart-portfolio-agent` (or your preferred name)
- **Region:** Choose closest to you (e.g., Oregon)
- **Branch:** `main`
- **Root Directory:** Leave blank
- **Runtime:** Python 3

**Build & Deploy:**
- **Build Command:** `pip install -r backend/requirements.txt`
- **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

**Instance Type:**
- Select **"Free"** (sufficient for demo/testing)

### 4. Add Environment Variables

Click "Advanced" → "Add Environment Variable"

Add this required variable:
- **Key:** `OPENAI_API_KEY`
- **Value:** Your OpenAI API key (starts with `sk-...`)

Optional variables:
- `CAPITALCUBE_API_KEY` - If you have CapitalCube API access
- `REDIS_URL` - If you want to add caching (can add later)

### 5. Deploy!

1. Click "Create Web Service"
2. Wait 5-10 minutes for the build to complete
3. Watch the logs for any errors

### 6. Access Your App

Once deployed, Render will give you a URL like:
```
https://smart-portfolio-agent.onrender.com
```

Your app will be live at:
- **UI:** https://your-app.onrender.com/
- **API Docs:** https://your-app.onrender.com/docs
- **Health Check:** https://your-app.onrender.com/health

## 🎯 Post-Deployment

### Test Your Deployment
```bash
curl https://your-app.onrender.com/health
```

### View Logs
- Go to your Render dashboard
- Click on your service
- Click "Logs" to see real-time logs

### Update Your App
Simply push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
```
Render will auto-deploy! 🎉

## ⚠️ Important Notes

### Free Tier Limitations
- Service spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds (cold start)
- 750 hours/month free (sufficient for demo/testing)

### Upgrade to Paid (Optional)
- **Starter ($7/month):** Always on, no cold starts
- **Standard ($25/month):** More resources, custom domains

## 🐛 Troubleshooting

### Build Fails
- Check `backend/requirements.txt` is correct
- Verify Python version compatibility
- Check Render logs for specific error

### App Crashes
- Verify `OPENAI_API_KEY` is set correctly
- Check application logs in Render dashboard
- Ensure all dependencies are installed

### Can't Access App
- Check service status is "Live" (green)
- Wait for initial deployment to complete
- Try health endpoint first: `/health`

## 📚 Resources

- [Render Python Docs](https://render.com/docs/deploy-fastapi)
- [Render Environment Variables](https://render.com/docs/environment-variables)
- [Render Free Tier](https://render.com/docs/free)

---

**Need Help?** Check the logs in your Render dashboard or review the official Render documentation.

