# 📋 Render Deployment Checklist & Configuration

## ✅ Pre-Deployment Verification

### Files Required
```
✅ requirements.txt        (at repo root)
✅ Procfile               (at repo root)
✅ backend/api.py          (main app)
✅ backend/*.py            (all modules)
✅ .env.example            (template)
✅ render.yaml             (optional, Render auto-detects)
```

### Verify All Files Exist
```bash
ls -la requirements.txt
ls -la Procfile
ls -la backend/api.py
```

---

## 🔧 Environment Variables for Render

### Required
| Variable | Value | Purpose |
|----------|-------|---------|
| `FLASK_ENV` | `production` | Flask mode |
| `FLASK_DEBUG` | `false` | Disable debug mode |
| `PYTHONUNBUFFERED` | `true` | Real-time logging |

### Optional but Recommended
| Variable | Value | Purpose |
|----------|-------|---------|
| `JWT_SECRET_KEY` | `<generate>` | Session security |
| `LOG_FILE` | `audit.log` | Log output file |
| `MAX_CONTENT_LENGTH` | `5242880` | Max file size (5MB) |
| `RATE_LIMIT_ENABLED` | `true` | Enable rate limiting |

### Generate JWT Secret
```bash
# Run this locally
python3 -c "import secrets; print(secrets.token_hex(32))"

# Example output:
# a7f2c9e1b4d6f8h2j5k7l9m1n3p5q7r9s1t3u5v7w9x1y3z5a7b9c1d3e5f7

# Copy output and paste into Render dashboard
```

---

## 🚀 Step-by-Step Render Setup

### Step 1: Prepare GitHub
```bash
# Make sure all changes are committed
git add .
git commit -m "Add Render deployment configuration"
git push origin main

# Verify on GitHub that all files are there
# Check: requirements.txt, Procfile, backend/ directory
```

### Step 2: Render Account Setup
1. Go to https://render.com
2. Click **"Sign up"** (or log in)
3. Verify email
4. Create account

### Step 3: Connect GitHub
1. Click **"Dashboard"**
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect a repository"**
4. Authorize Render to access GitHub
5. Select `pharmaguard` repository
6. Click **"Connect"**

### Step 4: Configure Service
Fill in the form:

| Field | Value |
|-------|-------|
| **Name** | `pharmaguard-api` |
| **Environment** | `Python 3` |
| **Region** | Choose closest (e.g., Ohio, Frankfurt) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt && cd backend && python -m pip install -r requirements.txt` |
| **Start Command** | `cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT api:app` |
| **Plan** | `Free` (testing) or `Starter` (production) |

### Step 5: Add Environment Variables
1. Scroll down to **"Advanced"**
2. Click **"Add Environment Variable"**
3. Add each variable:

```
FLASK_ENV = production
FLASK_DEBUG = false
PYTHONUNBUFFERED = true
LOG_FILE = audit.log
JWT_SECRET_KEY = <your-generated-secret>
MAX_CONTENT_LENGTH = 5242880
RATE_LIMIT_ENABLED = true
```

### Step 6: Deploy
1. Click **"Create Web Service"**
2. Wait for build (2-5 minutes)
3. Check **"Logs"** tab for success message
4. Once deployed, you'll see a URL like:
   ```
   https://pharmaguard-api-xxxx.onrender.com
   ```

---

## 🧪 Testing Your Deployment

### Test 1: Health Check
```bash
# Replace with your actual Render URL
curl https://pharmaguard-api-xxxx.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-19T10:30:45.123456"
}
```

### Test 2: API Analysis
```bash
curl -X POST https://pharmaguard-api-xxxx.onrender.com/analyze \
  -F "patient_id=TEST001" \
  -F "drug=CODEINE" \
  -F "vcf_file=@backend/test_sample.vcf"
```

Expected response:
```json
{
  "analysis_id": "...",
  "patient_id": "TEST001",
  "drug": "CODEINE",
  "risk_assessment": {
    "risk_label": "Safe",
    "risk_score": 0.0,
    ...
  }
}
```

### Test 3: Rate Limiting
```bash
# Make 21 requests in quick succession
for i in {1..21}; do
  curl https://pharmaguard-api-xxxx.onrender.com/health
done

# After 20th request, should get 429 (Too Many Requests)
# This proves rate limiting is working!
```

---

## 📊 Monitoring on Render Dashboard

### View Logs
```
Dashboard → Your Service → Logs
```
Shows real-time output from your app.

### View Metrics
```
Dashboard → Your Service → Metrics
```
Monitor:
- CPU usage
- Memory usage
- Request count
- Response times

### View Events
```
Dashboard → Your Service → Events
```
Shows deployment history.

### Check Status
- 🟢 Live = Service is running
- 🟡 Deploying = Build in progress
- 🔴 Failed = Something went wrong

---

## 🔄 Continuous Deployment

Render automatically redeploys when you push to GitHub:

```bash
# Make a change to your code
echo "# Updated" >> README.md

# Commit and push
git add README.md
git commit -m "Update README"
git push origin main

# Render automatically redeploys!
# Check Dashboard → Events to see the deployment progress
```

To **disable auto-deploy**:
- Dashboard → Settings → Disable Auto-Deploy

---

## 🆘 Troubleshooting

### Build Fails

**Error**: `ModuleNotFoundError: No module named 'flask'`
- **Cause**: `requirements.txt` not found
- **Fix**: 
  ```bash
  ls -la requirements.txt
  git add requirements.txt
  git push origin main
  ```

**Error**: `Build command failed`
- **Check logs** in Render dashboard
- **Verify** Python version (should be 3.8+)
- **Try locally**:
  ```bash
  pip install -r requirements.txt
  cd backend && python -m pip install -r requirements.txt
  ```

### Service Won't Start

**Error**: `Cannot find 'api.py'`
- **Cause**: Start command is wrong
- **Check**: 
  ```bash
  ls -la backend/api.py
  ```
- **Fix**: Make sure start command includes `cd backend`

**Error**: `Port 5000 is already in use`
- **Fix**: Your start command should use `$PORT` variable (already correct in Procfile)

### Health Check Returns 502

**Error**: `Bad Gateway`
- **Cause**: Flask app crashed
- **Fix**:
  1. Check Render logs for error message
  2. Test locally: `python -m backend.api`
  3. Verify all imports work: `python -c "from backend.api import app"`

**Error**: `Connection refused`
- **Cause**: Flask not listening on correct port
- **Check**: Your start command uses `0.0.0.0:$PORT`

### Rate Limiting Not Working

**Error**: Can make unlimited requests
- **Cause**: `RATE_LIMIT_ENABLED` is false
- **Fix**: Set `RATE_LIMIT_ENABLED=true` in environment variables
- **Restart**: Click "Manual Deploy" button

---

## 💾 Logs & Debugging

### View Logs in Real-time
```
Dashboard → Logs (scroll down to see latest)
```

### Search Logs for Errors
```
Dashboard → Logs → Search for "error" or "ERROR"
```

### Common Log Messages

**Success**:
```
Running on http://0.0.0.0:5000 (Press CTRL+C to quit)
```

**Error**:
```
Traceback (most recent call last): ...
```

**Startup**:
```
Starting PharmGuard API Server
```

---

## 🎯 Render Features

### Free Tier
- ✅ Deploy and test
- ✅ Auto-HTTPS
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ Shared resources

### Starter Tier ($7/month)
- ✅ Always on
- ✅ Dedicated resources
- ✅ Priority support
- ✅ Better performance

### Production Tier ($25/month)
- ✅ High availability
- ✅ Dedicated resources
- ✅ 99.9% uptime SLA
- ✅ Auto-scaling

---

## 🔗 Your API URLs

Once deployed:

```
Base URL:
https://pharmaguard-api-xxxx.onrender.com

Endpoints:
GET  /health           Health check
POST /analyze          Main analysis

Example requests:
curl https://pharmaguard-api-xxxx.onrender.com/health
curl -X POST https://pharmaguard-api-xxxx.onrender.com/analyze \
  -F "patient_id=P001" \
  -F "drug=CODEINE" \
  -F "vcf_file=@test.vcf"
```

---

## 📱 Frontend Integration

If you have a frontend, point it to your Render URL:

```javascript
const API_URL = "https://pharmaguard-api-xxxx.onrender.com";

// Health check
fetch(`${API_URL}/health`)
  .then(r => r.json())
  .then(data => console.log(data));

// Analyze
const formData = new FormData();
formData.append("patient_id", "P001");
formData.append("drug", "CODEINE");
formData.append("vcf_file", fileInput.files[0]);

fetch(`${API_URL}/analyze`, {
  method: "POST",
  body: formData
})
  .then(r => r.json())
  .then(data => console.log(data));
```

---

## ✨ You're Live!

Your PharmaGuard API is now accessible worldwide:

```
https://pharmaguard-api-xxxx.onrender.com
```

**Next Steps:**
1. Share URL with team
2. Integrate with frontend
3. Monitor metrics
4. Upgrade plan if needed

---

## 📚 Quick Reference

| Task | How To |
|------|--------|
| Restart service | Dashboard → Manual Deploy |
| Update code | Push to GitHub (auto-deploys) |
| View logs | Dashboard → Logs |
| Change variables | Dashboard → Environment |
| Check metrics | Dashboard → Metrics |
| Scale up | Dashboard → Settings → Plan |
| Add custom domain | Dashboard → Settings → Custom Domain |

---

## ✅ Success Checklist

- [ ] Code pushed to GitHub
- [ ] requirements.txt exists at root
- [ ] Procfile is correct
- [ ] Render account created
- [ ] GitHub connected to Render
- [ ] Environment variables set
- [ ] Build successful (green)
- [ ] Health endpoint responds
- [ ] API works with test VCF
- [ ] Rate limiting verified
- [ ] Logs monitored
- [ ] URL shared with team

---

**🎉 Deployment Complete!**

Your PharmaGuard backend is now running on Render!

Need help? See:
- [RENDER_QUICK_START.md](RENDER_QUICK_START.md)
- [SECURITY.md](SECURITY.md)
- [README.md](README.md)
