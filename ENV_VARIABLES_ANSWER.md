# 🎯 ENVIRONMENT VARIABLES - YOUR COMPLETE ANSWER

## 📌 ANSWER TO YOUR QUESTION

**"What variable names and values do I need for Render?"**

Here are the **EXACT variable names and values** you must enter:

---

## ✅ 4 REQUIRED VARIABLES

### Variable 1:
```
Name:  FLASK_ENV
Value: production
```

### Variable 2:
```
Name:  FLASK_DEBUG
Value: false
```

### Variable 3:
```
Name:  PYTHONUNBUFFERED
Value: true
```

### Variable 4: ⭐ IMPORTANT
```
Name:  JWT_SECRET_KEY
Value: <Generate yourself - see below>
```

---

## 🔐 HOW TO GET JWT_SECRET_KEY VALUE

### Step 1: Open Terminal
Open PowerShell or Command Prompt on your computer

### Step 2: Run This Command
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Step 3: You'll Get
```
a7f2c9e1b4d6f8h2j5k7l9m1n3p5q7r9s1t3u5v7w9x1y3z5a7b9c1d3e5f7
```

### Step 4: Copy It
Copy that entire long string

### Step 5: Use As JWT_SECRET_KEY Value
In Render, paste this value for JWT_SECRET_KEY

---

## 📋 ALL 4 IN A TABLE

| Variable Name | Value You Enter |
|---------------|-----------------|
| `FLASK_ENV` | `production` |
| `FLASK_DEBUG` | `false` |
| `PYTHONUNBUFFERED` | `true` |
| `JWT_SECRET_KEY` | `a7f2c9e1b4d...` (your generated key) |

---

## 🎯 OPTIONAL VARIABLES (Can Add)

| Variable Name | Value You Enter |
|---------------|-----------------|
| `LOG_FILE` | `audit.log` |
| `MAX_CONTENT_LENGTH` | `5242880` |
| `RATE_LIMIT_ENABLED` | `true` |

---

## 📝 HOW TO ENTER IN RENDER

### In Render Dashboard:

1. Open your service: `pharmaguard-api`
2. Click **Settings** (left sidebar)
3. Scroll to **Environment Variables**
4. Click **Add Environment Variable**

### Form appears:
```
Key:   [__________________________]
Value: [__________________________]
[Save]  [Cancel]
```

### Enter exactly like this:
```
Key:   FLASK_ENV
Value: production
[Save]
```

### Do this 4 times for all required variables

---

## ✨ COPY & PASTE EXACT TEXT

### For Variable 1:
```
Name: FLASK_ENV
Value: production
```

### For Variable 2:
```
Name: FLASK_DEBUG
Value: false
```

### For Variable 3:
```
Name: PYTHONUNBUFFERED
Value: true
```

### For Variable 4:
```
Name: JWT_SECRET_KEY
Value: [PASTE YOUR GENERATED SECRET HERE]
```

---

## 🎬 COMPLETE STEP-BY-STEP

### 1️⃣ Generate JWT Secret (on your computer)
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```
Copy the result

### 2️⃣ Go to Render Dashboard
Log in to render.com

### 3️⃣ Open Your Service
Click on `pharmaguard-api`

### 4️⃣ Settings
Click **Settings** (left sidebar)

### 5️⃣ Environment Variables
Scroll down to find it

### 6️⃣ Add Variable #1
```
Click "Add Environment Variable"
Key:   FLASK_ENV
Value: production
Click "Save"
```

### 7️⃣ Add Variable #2
```
Click "Add Environment Variable"
Key:   FLASK_DEBUG
Value: false
Click "Save"
```

### 8️⃣ Add Variable #3
```
Click "Add Environment Variable"
Key:   PYTHONUNBUFFERED
Value: true
Click "Save"
```

### 9️⃣ Add Variable #4
```
Click "Add Environment Variable"
Key:   JWT_SECRET_KEY
Value: [PASTE YOUR GENERATED SECRET]
Click "Save"
```

### 🔟 Optional: Add More (Recommended)
```
Repeat steps for:
- LOG_FILE = audit.log
- MAX_CONTENT_LENGTH = 5242880
- RATE_LIMIT_ENABLED = true
```

### ✅ Deploy
Click **"Create Web Service"** or **"Manual Deploy"**

---

## ⚠️ IMPORTANT NOTES

### Values Must Be EXACT
- ❌ Don't use `False` → ✅ Use `false`
- ❌ Don't use `True` → ✅ Use `true`
- ❌ Don't use `Production` → ✅ Use `production`
- ❌ Don't add quotes → ✅ Just the value

### JWT_SECRET_KEY
- Must be generated locally (use python command)
- Must be 64 characters long
- Must be unique per deployment
- Must be kept secret
- Must be copied exactly

---

## 📊 WHAT EACH VARIABLE DOES

| Variable | Purpose |
|----------|---------|
| `FLASK_ENV` | Tells Flask to run in secure mode |
| `FLASK_DEBUG` | Disables debug (for security) |
| `PYTHONUNBUFFERED` | Shows logs in real-time |
| `JWT_SECRET_KEY` | Security key for session signing |
| `LOG_FILE` | Where logs are saved |
| `MAX_CONTENT_LENGTH` | Maximum file size (5MB) |
| `RATE_LIMIT_ENABLED` | Protects from too many requests |

---

## ✅ FINAL CHECKLIST

Before clicking Deploy:

- [ ] Generated JWT_SECRET_KEY? (run python command)
- [ ] Copied the long string?
- [ ] Added FLASK_ENV = production?
- [ ] Added FLASK_DEBUG = false?
- [ ] Added PYTHONUNBUFFERED = true?
- [ ] Added JWT_SECRET_KEY = <your secret>?
- [ ] All values exactly correct?
- [ ] No extra spaces or quotes?

✅ Yes to all? → **READY TO DEPLOY!**

---

## 📁 Files for Reference

- **ENV_VARS_MASTER_GUIDE.txt** - Full visual guide
- **ENV_VARS_QUICK_REFERENCE.md** - Quick card
- **ENV_VARS_VISUAL_GUIDE.md** - Step-by-step visual
- **ENVIRONMENT_VARIABLES.md** - Complete details

---

## 🚀 YOU'RE READY!

You now have **exactly** what you need:

✅ Variable names  
✅ Variable values  
✅ How to generate JWT_SECRET_KEY  
✅ Where to add them in Render  
✅ Step-by-step instructions  

**Next: Add these variables to Render and deploy!** 🎉
