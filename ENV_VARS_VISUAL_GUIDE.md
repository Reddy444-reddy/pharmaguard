# 🎯 ENVIRONMENT VARIABLES - STEP BY STEP VISUAL GUIDE

## 📋 WHAT YOU NEED TO ENTER IN RENDER

### ✅ REQUIRED (4 Variables - Must Have)

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Variable #1:                                          │
│  ┌─────────────────────────────────────────────────┐  │
│  │ Key:   FLASK_ENV                               │  │
│  │ Value: production                               │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  Variable #2:                                          │
│  ┌─────────────────────────────────────────────────┐  │
│  │ Key:   FLASK_DEBUG                             │  │
│  │ Value: false                                    │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  Variable #3:                                          │
│  ┌─────────────────────────────────────────────────┐  │
│  │ Key:   PYTHONUNBUFFERED                         │  │
│  │ Value: true                                     │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  Variable #4: ⭐ IMPORTANT                             │
│  ┌─────────────────────────────────────────────────┐  │
│  │ Key:   JWT_SECRET_KEY                          │  │
│  │ Value: a7f2c9e1b4d6f8h2j5k7l9m1n3p5q7r9s1t... │  │
│  │        (your generated 64-char secret)         │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔐 STEP 1: GENERATE JWT_SECRET_KEY

### On Your Computer, Run:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### You Get Something Like:
```
a7f2c9e1b4d6f8h2j5k7l9m1n3p5q7r9s1t3u5v7w9x1y3z5a7b9c1d3e5f7
```

### 📌 Copy this value! You'll need it.

---

## 🌐 STEP 2: ADD TO RENDER DASHBOARD

### In Render Dashboard:

```
1. Open your Service (pharmaguard-api)
2. Click "Settings" (left sidebar)
3. Scroll down to "Environment Variables"
4. Click "Add Environment Variable"
   
   📝 Enter:
   
   Key:   FLASK_ENV
   Value: production
   
   Click "Save"
```

### Repeat for Each Variable:

```
┌─────────────────────────────────────────┐
│ Add Environment Variable                │
├─────────────────────────────────────────┤
│ Key:   [FLASK_ENV_______________________]│
│ Value: [production____________________]│
│        [Save] [Cancel]                  │
└─────────────────────────────────────────┘
```

---

## 📝 ALL 4 REQUIRED VARIABLES (Order Doesn't Matter)

### Variable 1
```
Key:   FLASK_ENV
Value: production
```
✅ Puts Flask in production mode (secure)

### Variable 2
```
Key:   FLASK_DEBUG
Value: false
```
✅ Disables debug mode (secure)

### Variable 3
```
Key:   PYTHONUNBUFFERED
Value: true
```
✅ Shows real-time logs

### Variable 4 ⭐
```
Key:   JWT_SECRET_KEY
Value: <your-generated-64-character-secret>
```
✅ Security key (MUST BE UNIQUE!)

---

## 📋 OPTIONAL BUT RECOMMENDED (3 More Variables)

```
┌─────────────────────────────────────────┐
│ Variable #5 (Optional)                  │
│ ┌───────────────────────────────────┐  │
│ │ Key:   LOG_FILE                   │  │
│ │ Value: audit.log                  │  │
│ └───────────────────────────────────┘  │
│                                         │
│ Variable #6 (Optional)                  │
│ ┌───────────────────────────────────┐  │
│ │ Key:   MAX_CONTENT_LENGTH         │  │
│ │ Value: 5242880                    │  │
│ └───────────────────────────────────┘  │
│                                         │
│ Variable #7 (Optional)                  │
│ ┌───────────────────────────────────┐  │
│ │ Key:   RATE_LIMIT_ENABLED         │  │
│ │ Value: true                       │  │
│ └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

---

## 🚀 COMPLETE CHECKLIST

### ✅ Before Adding Variables:
- [ ] Generated JWT_SECRET_KEY (run python command)
- [ ] Have the value copied
- [ ] Know the 3 other required variables
- [ ] Ready to add to Render

### ✅ While Adding Variables:
- [ ] Opened Render Dashboard
- [ ] Clicked on your service (pharmaguard-api)
- [ ] Went to Settings → Environment Variables
- [ ] Starting to add first variable (FLASK_ENV)

### ✅ After Adding Variables:
- [ ] Added all 4 required variables
- [ ] Values match exactly (especially lowercase `false`/`true`)
- [ ] JWT_SECRET_KEY is pasted correctly
- [ ] Clicked Save for each variable

### ✅ Final Step:
- [ ] Click "Create Web Service" OR "Manual Deploy"
- [ ] Wait for service to restart
- [ ] Check Logs for "Running on..." message
- [ ] Test health endpoint

---

## 📊 SIDE-BY-SIDE REFERENCE

```
╔════════════════════════╦════════════════════════════╗
║ Variable Name          ║ Value                      ║
╠════════════════════════╬════════════════════════════╣
║ FLASK_ENV              ║ production                 ║
║ FLASK_DEBUG            ║ false                      ║
║ PYTHONUNBUFFERED       ║ true                       ║
║ JWT_SECRET_KEY         ║ a7f2c9e1b4d6f8h2j5k...   ║
║ (OPTIONAL)             ║                            ║
║ LOG_FILE               ║ audit.log                  ║
║ MAX_CONTENT_LENGTH     ║ 5242880                    ║
║ RATE_LIMIT_ENABLED     ║ true                       ║
╚════════════════════════╩════════════════════════════╝
```

---

## 🎯 COPY & PASTE READY

### Your Exact Template:

```
FLASK_ENV = production
FLASK_DEBUG = false
PYTHONUNBUFFERED = true
JWT_SECRET_KEY = [PASTE YOUR GENERATED KEY HERE]
LOG_FILE = audit.log (optional)
MAX_CONTENT_LENGTH = 5242880 (optional)
RATE_LIMIT_ENABLED = true (optional)
```

---

## ✨ AFTER DEPLOYMENT

### Your Service Will Have:
- ✅ Production-grade security
- ✅ HTTPS enabled (free SSL)
- ✅ Rate limiting active
- ✅ Real-time logging
- ✅ File size limits

### Check Status:
```
Go to: Render Dashboard → Your Service → Logs

Look for: "Running on http://0.0.0.0:..."

If you see this → ✅ Success!
```

---

## ❓ QUICK Q&A

**Q: Exact value for FLASK_DEBUG?**  
A: `false` (lowercase, no quotes)

**Q: Exact value for PYTHONUNBUFFERED?**  
A: `true` (lowercase, no quotes)

**Q: Where to get JWT_SECRET_KEY value?**  
A: Run: `python3 -c "import secrets; print(secrets.token_hex(32))"`

**Q: Can I skip optional variables?**  
A: Yes, but recommended to add them

**Q: Do I need OPENAI_API_KEY?**  
A: Only if you want LLM explanations (optional)

**Q: What if I make a mistake?**  
A: Edit the variable in Render, click Save, service restarts

---

## 📱 MOBILE-FRIENDLY VERSION

### 4 Required Variables:
```
1. FLASK_ENV = production
2. FLASK_DEBUG = false
3. PYTHONUNBUFFERED = true
4. JWT_SECRET_KEY = <run python command>
```

### 3 Optional Variables:
```
5. LOG_FILE = audit.log
6. MAX_CONTENT_LENGTH = 5242880
7. RATE_LIMIT_ENABLED = true
```

---

## 🎬 NEXT STEP

1. **Generate JWT_SECRET_KEY** (python command)
2. **Go to Render Dashboard**
3. **Add 4 required variables** (exact values above)
4. **Click Deploy**
5. **Wait 5 minutes**
6. **Test your API** 🎉

---

**Ready? Go add these variables to Render! 🚀**
