# 🚀 Quick Render Deployment Checklist

## ✅ Pre-Deployment (5 minutes)

- [ ] Push latest code to GitHub
- [ ] Verify `requirements.txt` at root directory
- [ ] Verify `Procfile` exists and is correct
- [ ] All files committed and pushed

```bash
# Verify files exist
git status
git push origin main
```

---

## 🔐 Generate JWT Secret (1 minute)

```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_hex(32))"
```

Save this value - you'll need it in Render dashboard.

Example output:
```
a7f2c9e1b4d6f8h2j5k7l9m1n3p5q7r9s1t3u5v7w9x1y3z5a7b9c1d3e5f7
```

---

## 🌐 Render Deployment (10 minutes)

### Step 1: Create Service
1. Go to https://render.com
2. Click **New +** → **Web Service**
3. Click **Connect a repository**
4. Select your `pharmaguard` repository
5. Click **Connect**

### Step 2: Basic Configuration
- **Name**: `pharmaguard-api`
- **Environment**: `Python 3`
- **Region**: Choose closest to you
- **Plan**: `Free` (for testing) or `Starter` (for production)

### Step 3: Build & Start Commands
Should auto-fill from Procfile, verify:

**Build Command**:
```
pip install -r requirements.txt && cd backend && python -m pip install -r requirements.txt
```

**Start Command**:
```
cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT api:app
```

### Step 4: Environment Variables
Click **Advanced** → **Add from .env.example** or manually add:

```
FLASK_ENV=production
FLASK_DEBUG=false
PYTHONUNBUFFERED=true
LOG_FILE=audit.log
JWT_SECRET_KEY=<paste_your_generated_secret>
MAX_CONTENT_LENGTH=5242880
RATE_LIMIT_ENABLED=true
```

### Step 5: Deploy
- Click **Create Web Service**
- Wait for build to complete (3-5 minutes)
- Check logs for success message

---

## 🧪 Post-Deployment (5 minutes)

### Get Your URL
From Render dashboard, copy your service URL:
```
https://pharmaguard-api-xxxx.onrender.com
```

### Test Health Endpoint
```bash
curl https://pharmaguard-api-xxxx.onrender.com/health
```

Expected:
```json
{"status": "healthy", "timestamp": "..."}
```

### Test API Endpoint
```bash
curl -X POST https://pharmaguard-api-xxxx.onrender.com/analyze \
  -F "patient_id=TEST001" \
  -F "drug=CODEINE" \
  -F "vcf_file=@backend/test_sample.vcf"
```

---

## 📊 Monitor & Manage

### View Real-time Logs
Render Dashboard → **Logs** tab

### Restart Service
Render Dashboard → **Manual deploy** button

### Update Code
Just push to GitHub - auto-deploys!

```bash
git add .
git commit -m "Update configuration"
git push origin main
```

### Check Metrics
Render Dashboard → **Metrics** tab

---

## 🆘 If Something Goes Wrong

### Check Build Logs
1. Go to Render Dashboard
2. Click **Events** tab
3. Look for build errors

### Common Issues

**❌ ModuleNotFoundError: No module named 'flask'**
- Fix: Make sure `requirements.txt` exists at root
- Check: `pip install -r requirements.txt` works locally

**❌ Cannot find 'api.py'**
- Fix: Start command must include `cd backend`
- Check: `cd backend && gunicorn api:app` works locally

**❌ /health endpoint returns 502**
- Check logs: Render Dashboard → Logs
- Verify: Start command is correct
- Check: Flask app listens on `0.0.0.0:$PORT`

**❌ Port binding error**
- Don't hardcode port - use `$PORT` environment variable
- Already correct in your `Procfile` ✅

---

## 🎯 Success Indicators

✅ Build succeeds (green checkmark)  
✅ Health endpoint responds  
✅ API endpoint accepts requests  
✅ Logs show no errors  
✅ Metrics show CPU/memory within limits  

---

## 📈 Tier Comparison

| Feature | Free | Starter | Professional |
|---------|------|---------|--------------|
| Cost | $0 | $7/mo | $25/mo |
| Always On | ❌ | ✅ | ✅ |
| CPU | 0.5 | 1 | 3 |
| RAM | 512MB | 512MB | 2GB |
| Spins Down | Yes (15 min) | No | No |
| Best For | Testing | Dev | Production |

---

## 🔗 Your Deployed API

```
Base URL: https://pharmaguard-api-xxxx.onrender.com

Endpoints:
- GET  /health           → Health check
- POST /analyze          → Main analysis endpoint
```

---

## 📱 Example Client Code

```python
import requests

BASE_URL = "https://pharmaguard-api-xxxx.onrender.com"

# Health check
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# Analyze VCF
files = {"vcf_file": open("test_sample.vcf", "rb")}
data = {"patient_id": "P001", "drug": "CODEINE"}
response = requests.post(f"{BASE_URL}/analyze", files=files, data=data)
print(response.json())
```

---

## ✨ You're Live!

Once deployed, your API is accessible worldwide at:

```
https://pharmaguard-api-xxxx.onrender.com
```

Share this URL with teammates, frontend developers, or integrate it into your application!

---

**Need Help?**
- Render Docs: https://render.com/docs
- GitHub Integration: https://render.com/docs/github
- See `RENDER_DEPLOYMENT.md` for detailed guide

🎉 **Congratulations on your deployment!**
