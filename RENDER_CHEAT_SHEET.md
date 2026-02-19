# 🎯 RENDER DEPLOYMENT - QUICK REFERENCE CARD

## 📋 Before You Start

```
✅ Code committed to GitHub
✅ requirements.txt at root
✅ Procfile configured
✅ Have JWT secret ready (run: python -c "import secrets; print(secrets.token_hex(32))")
```

---

## 🚀 DEPLOYMENT IN 5 STEPS

### 1️⃣ PUSH CODE (1 min)
```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

### 2️⃣ GO TO RENDER (1 min)
```
https://render.com → New + → Web Service → Select GitHub repo
```

### 3️⃣ BASIC CONFIG (2 min)
```
Name: pharmaguard-api
Environment: Python 3
Region: Closest to you
Plan: Free (test) or Starter (production)
```

### 4️⃣ BUILD & START (Auto-filled)
```
Build:  pip install -r requirements.txt && cd backend && python -m pip install -r requirements.txt
Start:  cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT api:app
```

### 5️⃣ ENVIRONMENT VARIABLES (2 min)
```
FLASK_ENV = production
FLASK_DEBUG = false
PYTHONUNBUFFERED = true
JWT_SECRET_KEY = <your generated secret>
```

Click **"Create Web Service"** → Wait 5 min → ✅ LIVE!

---

## 🧪 TEST YOUR API

```bash
# Get your URL from Render dashboard
URL="https://pharmaguard-api-xxxx.onrender.com"

# Health check
curl $URL/health

# Full test
curl -X POST $URL/analyze \
  -F "patient_id=P001" \
  -F "drug=CODEINE" \
  -F "vcf_file=@backend/test_sample.vcf"
```

---

## 📚 WHICH GUIDE TO READ?

| Situation | Guide |
|-----------|-------|
| **First time deploying?** | RENDER_QUICK_START.md |
| **Want detailed walkthrough?** | RENDER_DETAILED_SETUP.md |
| **Need quick overview?** | RENDER_DEPLOY_NOW.md |
| **Have questions?** | RENDER_DETAILED_SETUP.md (Troubleshooting section) |
| **Security concerns?** | SECURITY.md |

---

## 🔗 YOUR DEPLOYED URL

After deployment (5-10 min):
```
https://pharmaguard-api-xxxx.onrender.com

Use this URL to:
- Call the API
- Share with team
- Integrate with frontend
- Monitor in Render dashboard
```

---

## ✅ SUCCESS INDICATORS

- ✅ Render shows green status
- ✅ `/health` endpoint responds
- ✅ `/analyze` accepts requests
- ✅ Logs show no errors
- ✅ Metrics show normal CPU/memory

---

## 💰 PRICING

```
Free:         $0/month  (spins down after 15 min idle)
Starter:      $7/month  (always on)
Professional: $25/month (auto-scaling)
```

Start free, upgrade anytime!

---

## 🔑 JWT SECRET GENERATION

```bash
# Run locally
python3 -c "import secrets; print(secrets.token_hex(32))"

# Copy output, paste as JWT_SECRET_KEY in Render
```

---

## 📞 QUICK HELP

| Issue | Solution |
|-------|----------|
| Build fails | Check logs, verify requirements.txt exists |
| /health 502 | Check Start command, Flask listening on 0.0.0.0:$PORT |
| Can't import module | Verify all files pushed to GitHub |
| Rate limiting test | Make >20 requests/hour, should get 429 on /analyze |
| Want to update code | Push to GitHub, Render auto-redeploys |

---

## 🎯 DEPLOYMENT CHECKLIST

- [ ] Run: `git push origin main`
- [ ] Go to: https://render.com
- [ ] Create Web Service from GitHub
- [ ] Set Name: `pharmaguard-api`
- [ ] Set Environment: `Python 3`
- [ ] Verify Build & Start commands (auto-filled)
- [ ] Add environment variables (5 variables)
- [ ] Generate & add JWT_SECRET_KEY
- [ ] Click "Create Web Service"
- [ ] Wait for green status (5-10 min)
- [ ] Test health endpoint
- [ ] Share URL with team

---

## 🎉 YOU'RE READY!

Your backend is deployment-ready right now.

**Start here:** [START_HERE_RENDER.md](START_HERE_RENDER.md)

**Questions?** See [RENDER_QUICK_START.md](RENDER_QUICK_START.md)

**Go live:** https://render.com

🚀 **Let's deploy!**

---

## 📊 DEPLOYMENT TIMELINE

```
Step 1 (Push):        <1 min  ✅
Step 2 (Render UI):   2 min   ⏳
Step 3 (Config):      2 min   ⏳
Step 4 (Build):       3 min   ⏳
Step 5 (Deploy):      1 min   ⏳
────────────────────────────────
TOTAL:               ~9 min   🚀 LIVE!
```

---

**Next Step:** Go to https://render.com or read [START_HERE_RENDER.md](START_HERE_RENDER.md)
