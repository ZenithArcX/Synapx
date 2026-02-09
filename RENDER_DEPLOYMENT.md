# Deployment on Render

This guide walks you through deploying the Insurance Claims Agent to Render.com for free.

## What You'll Deploy

- **Backend API** (Python Flask) → Web Service
- **Frontend UI** (React) → Static Site

Both will be live on Render's subdomains.

## Prerequisites

1. GitHub repo: https://github.com/ZenithArcX/Synapx.git
2. Render account: https://render.com (free)
3. Code pushed to GitHub

## Step 1: Push Code to GitHub

```bash
cd /mnt/data/projects/SYNAPX/insurance-claims-agent

# Configure git
git config --global user.name "zenitharcx"
git config --global user.email "sammetaakhilsai@gmail.com"

# Initialize and push
git init
git add .
git commit -m "Insurance Claims Agent - Ready for Render deployment"
git remote add origin https://github.com/ZenithArcX/Synapx.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy Backend on Render

1. Go to https://render.com and sign in
2. Click **"New +"** → **"Web Service"**
3. Select **GitHub repository**: `Synapx`
4. Configure:
   - **Name**: `claims-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python api_server.py`
   - **Region**: Choose closest to you (e.g., US)
   - **Plan**: Free
5. Click **"Create Web Service"**

**Wait for deployment** (takes 2-3 minutes)

Once done, you'll get a URL like: `https://claims-api-xxxxx.onrender.com`

**Copy this URL** - you'll need it in Step 4.

## Step 3: Deploy Frontend on Render

1. In Render dashboard, click **"New +"** → **"Static Site"**
2. Select **GitHub repository**: `Synapx`
3. Configure:
   - **Name**: `claims-web`
   - **Build Command**: `echo "Frontend ready"`
   - **Publish Directory**: `frontend`
   - **Plan**: Free
4. Click **"Create Static Site"**

**Wait for deployment**

You'll get a URL like: `https://claims-web-xxxxx.onrender.com`

## Step 4: Connect Frontend to Backend

The frontend needs to know where the backend API is hosted.

**Update frontend/app.js line 3:**

Find:
```javascript
const API_URL = (() => {
  if (window.location.hostname.includes('render.com')) {
    return 'https://claims-api.onrender.com';
  }
  // ...
})();
```

Replace `claims-api.onrender.com` with your actual backend URL from Step 2.

**Example:**
```javascript
return 'https://claims-api-abc123.onrender.com';
```

Then push the change:
```bash
git add frontend/app.js
git commit -m "Update API URL for Render deployment"
git push
```

Render will auto-redeploy the frontend.

## Step 5: Test Your Deployment

1. Open your frontend URL: `https://claims-web-xxxxx.onrender.com`
2. Try the **Manual Entry** tab
3. Fill in form and click **"Process Claim"**
4. Should get JSON response from backend

## URLs After Deployment

| Component | URL |
|-----------|-----|
| **Frontend** | https://claims-web-xxxxx.onrender.com |
| **API** | https://claims-api-xxxxx.onrender.com/api/claims/process |

## Cold Start Warning

First request takes ~30 seconds (free tier spins down after 15 min inactivity).

After first request, it's instant.

## Files Used for Deployment

- `render.yaml` - Render deployment config
- `Procfile` - Python startup command
- `requirements.txt` - Dependencies
- `api_server.py` - Flask app with CORS
- `frontend/app.js` - React UI with API_URL

## Monitoring Logs

In Render dashboard:
1. Click your service
2. Scroll to **"Logs"**
3. Watch logs in real-time

## Troubleshooting

### API returns 502 Bad Gateway
- Check backend logs in Render
- Ensure `Procfile` has correct start command
- Verify `requirements.txt` has all dependencies

### Frontend won't connect to API
- Check frontend API_URL matches backend URL
- Check CORS is enabled in `api_server.py`
- Check backend is actually running (logs show no errors)

### File uploads return error
- Free tier has memory limitations
- Large files might fail
- Test with small PDF first

## Next Steps

✅ Deploy to Render
✅ Test both endpoints
✅ Share frontend URL with team
✅ Monitor logs for issues

---

**Cost:** $0 (forever, with free tier)
**Uptime:** ~99% but can be ~30s cold starts
**Support:** Render has good docs: https://render.com/docs
