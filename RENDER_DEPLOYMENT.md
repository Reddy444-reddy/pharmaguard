# PharmaGuard Deployment Guide - Render

## ✅ Prerequisites

- GitHub account with your PharmaGuard repo
- Render account (https://render.com - free tier available)
- All changes pushed to GitHub

---

## 🚀 Step 1: Connect GitHub to Render

1. Go to https://render.com
2. Click **"New +"** → **"Web Service"**
3. Select **"Connect a repository"**
4. Authorize Render to access your GitHub account
5. Select your `pharmaguard` repository
6. Click **"Connect"**

---

## 🔧 Step 2: Configure the Service

### Basic Settings
- **Name**: `pharmaguard-api`
- **Environment**: `Python 3`
- **Region**: Select closest to you (e.g., `Ohio`, `Frankfurt`)
- **Plan**: `Free` (or `Starter` for production)

### Build & Start Commands
These should auto-detect from your `Procfile`, but verify:

**Build Command**:
```bash
pip install -r requirements.txt && cd backend && python -m pip install -r requirements.txt
```

**Start Command**:
```bash
cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT api:app
```

---

## 🔐 Step 3: Set Environment Variables

Click **"Advanced"** → **"Environment Variables"**

Add the following:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `FLASK_DEBUG` | `false` |
| `PYTHONUNBUFFERED` | `true` |
| `LOG_FILE` | `audit.log` |
| `JWT_SECRET_KEY` | Generate with: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `MAX_CONTENT_LENGTH` | `5242880` |
| `RATE_LIMIT_ENABLED` | `true` |

---

## 📦 Step 4: Verify Dependencies

Render will use your `requirements.txt`. Make sure it's at the repo root.

Check the root `requirements.txt` includes:
```
Flask==3.0.0
Flask-CORS==4.0.0
Flask-Limiter==3.5.0
pyvcf3==1.0.1
requests==2.31.0
gunicorn==21.2.0
python-dotenv==1.0.0
```

✅ Already configured in your repo!

---

## ✨ Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will start the build process
3. Monitor logs in the **"Events"** tab
4. Once deployed, you'll get a URL like: `https://pharmaguard-api-xxxx.onrender.com`

---

## 🧪 Step 6: Test Your Deployment

Once deployed, test the health endpoint:

```bash
curl https://pharmaguard-api-xxxx.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-19T10:30:45.123456"
}
```

Test with a sample request:
```bash
curl -X POST https://pharmaguard-api-xxxx.onrender.com/analyze \
  -F "patient_id=P001" \
  -F "drug=CODEINE" \
  -F "vcf_file=@test_sample.vcf"
```

---

## 🔄 Step 7: Auto-Deployment

Once connected:
- **Every push to main** → Automatic redeploy
- Check **"Auto-Deploy"** is enabled in settings
- Monitor deployments in the **"Deployments"** tab

---

## 📊 Monitoring on Render

### View Logs
- Go to your service dashboard
- Click **"Logs"** tab
- Real-time logs appear here

### Performance Metrics
- Click **"Metrics"** tab
- Monitor CPU, memory, requests

### Health Check
Render auto-monitors your `/health` endpoint

---

## 🆘 Troubleshooting

### Build Fails
Check build logs for:
- ❌ Missing dependencies → Update `requirements.txt`
- ❌ Python version → Render defaults to Python 3.10+
- ❌ Import errors → Check file paths

### Service Won't Start
```
Error: ModuleNotFoundError: No module named 'flask'
```
→ Make sure `requirements.txt` is in repo root and includes Flask

### Service Crashes
```
Error: Cannot find file 'api.py'
```
→ Verify start command: `cd backend && gunicorn ... api:app`

### Health Check Fails
```
GET /health returning 502
```
→ Check logs: `tail -f /tmp/render.log`
→ Ensure Flask app is listening on `0.0.0.0:$PORT`

### Rate Limiting Issues
```
Error: Flask-Limiter not found
```
→ Run: `pip install Flask-Limiter==3.5.0`
→ Ensure it's in `requirements.txt`

---

## 🔌 Database Connections (Optional)

If you add MongoDB for audit logs later:

```python
# In environment variables
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/pharmaguard
```

---

## 📈 Scaling Tips

### Free Tier Limitations
- ⚠️ Spins down after 15 min of inactivity
- ⚠️ 0.5 CPU, 512 MB RAM shared
- ✅ Good for development/testing

### Upgrade to Starter
- 🟢 Always on
- 🟢 1 CPU, 512 MB RAM
- 🟢 $7/month

### Production Tier
- 🟢 3 CPU, 2 GB RAM
- 🟢 99.9% uptime SLA
- 🟢 $25/month

---

## 🔒 Security Reminders

1. **Never commit `.env` file** ✅ Already in `.gitignore`
2. **Generate JWT secret** per environment
3. **Use HTTPS only** ✅ Render provides free SSL
4. **Monitor logs** for suspicious activity
5. **Update dependencies** regularly

---

## 📋 Render Dashboard Features

Once deployed, explore:
- **Logs** - Real-time application logs
- **Metrics** - CPU, memory, request stats
- **Events** - Deployment history
- **Environment** - Manage variables
- **Settings** - Configure service
- **Custom Domain** - Add your own domain

---

## 🎯 Your Render URL

After deployment:
```
https://pharmaguard-api-<random>.onrender.com
```

Share this URL for API access!

---

## 📚 Quick Reference

| Action | Command |
|--------|---------|
| View logs | Render Dashboard → Logs |
| Restart service | Dashboard → Manual deploy |
| Update code | Push to GitHub (auto-deploys) |
| Change variables | Dashboard → Environment |
| Monitor metrics | Dashboard → Metrics |

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] `requirements.txt` at root
- [ ] `Procfile` configured
- [ ] Render account created
- [ ] GitHub repo connected to Render
- [ ] Environment variables set
- [ ] Build successful
- [ ] Health endpoint responds
- [ ] Test API with sample VCF

---

## 🚀 Next Steps

1. **Go to Render**: https://render.com
2. **Create Web Service** from your GitHub repo
3. **Set environment variables** (at least FLASK_ENV=production)
4. **Deploy** and wait for green status
5. **Test** the health endpoint
6. **Monitor** logs in Render dashboard

---

**Need Help?**
- Render Docs: https://render.com/docs
- Check `SECURITY.md` for security settings
- Check `PRODUCTION_DEPLOYMENT.md` for advanced config

**Status**: ✅ Ready for Render Deployment!
