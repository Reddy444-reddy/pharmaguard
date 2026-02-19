# 🔑 Environment Variables for Render - Complete Reference

## 📋 All Variables You Need

Copy & paste this format into Render's environment variables section.

---

## ✅ REQUIRED Variables (Must Have)

### 1. FLASK_ENV
```
Variable Name:  FLASK_ENV
Value:          production
Purpose:        Sets Flask to production mode (disables debug)
```

### 2. FLASK_DEBUG
```
Variable Name:  FLASK_DEBUG
Value:          false
Purpose:        Disables debug mode (security)
```

### 3. PYTHONUNBUFFERED
```
Variable Name:  PYTHONUNBUFFERED
Value:          true
Purpose:        Real-time logging output
```

### 4. JWT_SECRET_KEY ⭐ IMPORTANT
```
Variable Name:  JWT_SECRET_KEY
Value:          <Generate your own - see below>
Purpose:        Secure session/auth key
```

---

## 🔐 How to Generate JWT_SECRET_KEY

Run this command **locally** on your computer:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

**Example output:**
```
a7f2c9e1b4d6f8h2j5k7l9m1n3p5q7r9s1t3u5v7w9x1y3z5a7b9c1d3e5f7
```

**Copy this value** → Paste it as the JWT_SECRET_KEY value in Render

---

## 📋 OPTIONAL Variables (Recommended)

### 5. LOG_FILE
```
Variable Name:  LOG_FILE
Value:          audit.log
Purpose:        Log file name
Optional:       Yes (default: audit.log)
```

### 6. MAX_CONTENT_LENGTH
```
Variable Name:  MAX_CONTENT_LENGTH
Value:          5242880
Purpose:        Max file size in bytes (5MB)
Optional:       Yes (default: 5242880)
```

### 7. RATE_LIMIT_ENABLED
```
Variable Name:  RATE_LIMIT_ENABLED
Value:          true
Purpose:        Enable rate limiting protection
Optional:       Yes (default: true)
```

### 8. OPENAI_API_KEY (Optional - Only if using LLM)
```
Variable Name:  OPENAI_API_KEY
Value:          sk-... (your OpenAI key)
Purpose:        LLM explanation generation
Optional:       Yes (leave blank if not using)
```

---

## 🎯 Minimum Setup (What You MUST Enter in Render)

```
FLASK_ENV          = production
FLASK_DEBUG         = false
PYTHONUNBUFFERED    = true
JWT_SECRET_KEY      = <your-generated-secret>
```

**That's it! These 4 are required.**

---

## 📝 Complete Setup (All Variables)

```
FLASK_ENV               = production
FLASK_DEBUG             = false
PYTHONUNBUFFERED        = true
JWT_SECRET_KEY          = <your-generated-secret>
LOG_FILE                = audit.log
MAX_CONTENT_LENGTH      = 5242880
RATE_LIMIT_ENABLED      = true
```

---

## 🖱️ HOW TO ADD IN RENDER DASHBOARD

### Steps:
1. Go to your Render Service Dashboard
2. Click **"Settings"** (left sidebar)
3. Scroll down to **"Environment Variables"**
4. Click **"Add Environment Variable"**
5. Fill in:
   - **Key**: `FLASK_ENV`
   - **Value**: `production`
6. Click **"Save"**
7. Repeat for each variable

### Visual Example:
```
┌─────────────────────────────────────┐
│ Environment Variables               │
├─────────────────────────────────────┤
│ Key               │ Value            │
├───────────────────┼──────────────────┤
│ FLASK_ENV         │ production       │
│ FLASK_DEBUG       │ false            │
│ PYTHONUNBUFFERED  │ true             │
│ JWT_SECRET_KEY    │ a7f2c9e1b4d...   │
│ LOG_FILE          │ audit.log        │
│ MAX_CONTENT_...   │ 5242880          │
│ RATE_LIMIT_...    │ true             │
└─────────────────────────────────────┘
```

---

## 🔄 Updating Variables Later

If you need to change a variable after deployment:
1. Go to Service Dashboard
2. Click **"Settings"**
3. Click the variable you want to edit
4. Change the value
5. Click **"Save"**
6. Render will restart your service automatically

---

## ✨ Quick Copy-Paste Format

### For MINIMUM setup:
```
FLASK_ENV=production
FLASK_DEBUG=false
PYTHONUNBUFFERED=true
JWT_SECRET_KEY=<paste-your-generated-secret-here>
```

### For COMPLETE setup:
```
FLASK_ENV=production
FLASK_DEBUG=false
PYTHONUNBUFFERED=true
JWT_SECRET_KEY=<paste-your-generated-secret-here>
LOG_FILE=audit.log
MAX_CONTENT_LENGTH=5242880
RATE_LIMIT_ENABLED=true
```

---

## 🚨 IMPORTANT NOTES

### ⚠️ JWT_SECRET_KEY
- **Generate it locally** (use the command above)
- **Make it unique** for your deployment
- **Keep it secret** (never share)
- **Don't hardcode** it in files
- **Paste exact value** into Render

### ⚠️ Do NOT Include
❌ Database passwords in plain text  
❌ API keys in code (always use env variables)  
❌ Hardcoded secrets  
❌ Test credentials

---

## 📊 Variable Reference Table

| Variable Name | Required | Value | Type |
|---------------|----------|-------|------|
| `FLASK_ENV` | ✅ Yes | `production` | String |
| `FLASK_DEBUG` | ✅ Yes | `false` | Boolean |
| `PYTHONUNBUFFERED` | ✅ Yes | `true` | Boolean |
| `JWT_SECRET_KEY` | ✅ Yes | `<generate>` | String |
| `LOG_FILE` | ⚠️ Optional | `audit.log` | String |
| `MAX_CONTENT_LENGTH` | ⚠️ Optional | `5242880` | Number |
| `RATE_LIMIT_ENABLED` | ⚠️ Optional | `true` | Boolean |
| `OPENAI_API_KEY` | ❌ Optional | `sk-...` | String |

---

## 🔍 Verify Your Setup

After adding environment variables:

1. Click **"Manual Deploy"** in your service dashboard
2. Wait for deployment to complete
3. Check **"Logs"** tab
4. Look for: `Running on http://0.0.0.0:...`
5. If no errors → ✅ Correct!

---

## 📝 Example Deployed Configuration

Once deployed, your backend will:
- ✅ Run in production mode
- ✅ Have HTTPS enabled (auto)
- ✅ Log to audit.log file
- ✅ Limit file uploads to 5MB
- ✅ Enforce rate limits
- ✅ Use secure JWT signing

---

## ❓ Questions?

### "Should I change FLASK_DEBUG?"
No - Always keep it `false` in production

### "Can I use a different JWT_SECRET_KEY?"
Yes - Generate a new one each time with the command

### "What if I forget JWT_SECRET_KEY?"
Generate a new one and update in Render dashboard

### "Do I need OPENAI_API_KEY?"
Only if you want LLM explanations (optional feature)

---

## 🎯 Final Checklist

Before clicking "Create Web Service":

- [ ] Have you generated JWT_SECRET_KEY? (python command)
- [ ] Do you have the 4 required variables ready?
- [ ] Have you read the values correctly?
- [ ] Are FLASK_DEBUG and PYTHONUNBUFFERED lowercase `false` and `true`?
- [ ] Is JWT_SECRET_KEY a long string (64+ characters)?

✅ Yes to all? → Ready to deploy!

---

## 🚀 Ready to Deploy?

1. **Copy the minimum 4 variables** from this guide
2. **Go to Render Dashboard** → Settings → Environment Variables
3. **Add each variable** one by one
4. **Verify JWT_SECRET_KEY** is pasted correctly
5. **Click "Create Web Service"**
6. **Wait 5-10 minutes**
7. **Done!** 🎉

---

**Need more help?** See [RENDER_QUICK_START.md](RENDER_QUICK_START.md) or [RENDER_DETAILED_SETUP.md](RENDER_DETAILED_SETUP.md)
