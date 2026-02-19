# 🔑 ENVIRONMENT VARIABLES - QUICK CARD

## 4 REQUIRED Variables (Copy & Paste into Render)

```
┌──────────────────────┬─────────────────────────────────────┐
│ Variable Name        │ Value                               │
├──────────────────────┼─────────────────────────────────────┤
│ FLASK_ENV            │ production                          │
│ FLASK_DEBUG          │ false                               │
│ PYTHONUNBUFFERED     │ true                                │
│ JWT_SECRET_KEY       │ <GENERATE - SEE BELOW>              │
└──────────────────────┴─────────────────────────────────────┘
```

---

## 🔐 GENERATE JWT_SECRET_KEY (Do This First!)

### Run this command on your computer:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### You'll get something like:
```
a7f2c9e1b4d6f8h2j5k7l9m1n3p5q7r9s1t3u5v7w9x1y3z5a7b9c1d3e5f7
```

### Copy this value → Paste as JWT_SECRET_KEY in Render

---

## 3 OPTIONAL Variables (Recommended)

```
┌──────────────────────┬──────────────┐
│ Variable Name        │ Value        │
├──────────────────────┼──────────────┤
│ LOG_FILE             │ audit.log    │
│ MAX_CONTENT_LENGTH   │ 5242880      │
│ RATE_LIMIT_ENABLED   │ true         │
└──────────────────────┴──────────────┘
```

---

## 📝 HOW TO ADD IN RENDER

1. Go to Render Dashboard
2. Click Settings (left sidebar)
3. Scroll to "Environment Variables"
4. Click "Add Environment Variable"
5. Enter:
   - **Key**: (e.g., `FLASK_ENV`)
   - **Value**: (e.g., `production`)
6. Click Save
7. Repeat for each variable

---

## ✅ MINIMUM You Need

```
FLASK_ENV          production
FLASK_DEBUG         false
PYTHONUNBUFFERED    true
JWT_SECRET_KEY      <your-generated-key>
```

---

## ✨ RECOMMENDED You Add

```
FLASK_ENV               production
FLASK_DEBUG             false
PYTHONUNBUFFERED        true
JWT_SECRET_KEY          <your-generated-key>
LOG_FILE                audit.log
MAX_CONTENT_LENGTH      5242880
RATE_LIMIT_ENABLED      true
```

---

## 🚨 IMPORTANT

✅ DO:
- Generate JWT_SECRET_KEY locally (use command above)
- Make it unique per deployment
- Use exact values (lowercase `false` and `true`)
- Keep secret key confidential

❌ DON'T:
- Share JWT_SECRET_KEY
- Hardcode secrets in code
- Use same key for all deployments
- Forget to generate it

---

## 📊 What Each Does

| Variable | Purpose |
|----------|---------|
| `FLASK_ENV` | Sets Flask mode (production = secure) |
| `FLASK_DEBUG` | Disables debug (false = secure) |
| `PYTHONUNBUFFERED` | Real-time logging |
| `JWT_SECRET_KEY` | Secure signing key |
| `LOG_FILE` | Where to save logs |
| `MAX_CONTENT_LENGTH` | Max file size (5MB) |
| `RATE_LIMIT_ENABLED` | Enable DDoS protection |

---

## 🎯 Copy & Paste Template

### STEP 1: Generate JWT_SECRET_KEY
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### STEP 2: Add to Render
```
Key: FLASK_ENV
Value: production

Key: FLASK_DEBUG
Value: false

Key: PYTHONUNBUFFERED
Value: true

Key: JWT_SECRET_KEY
Value: <PASTE-YOUR-GENERATED-KEY-HERE>
```

### STEP 3: (Optional) Add More
```
Key: LOG_FILE
Value: audit.log

Key: MAX_CONTENT_LENGTH
Value: 5242880

Key: RATE_LIMIT_ENABLED
Value: true
```

---

## ❓ Quick Answers

**Q: What's JWT_SECRET_KEY?**  
A: Security key for session signing (must be unique & secret)

**Q: How do I generate it?**  
A: Run: `python3 -c "import secrets; print(secrets.token_hex(32))"`

**Q: Can I use same JWT_SECRET_KEY for multiple deployments?**  
A: Not recommended - generate unique one for each

**Q: What if I lost my JWT_SECRET_KEY?**  
A: Generate a new one, update Render, restart service

**Q: Which variables are absolutely required?**  
A: The 4 at the top (FLASK_ENV, FLASK_DEBUG, PYTHONUNBUFFERED, JWT_SECRET_KEY)

**Q: Do I need OPENAI_API_KEY?**  
A: Only if using LLM explanations (optional feature)

---

## ✨ Final Check

Before deploying:
- [ ] Generated JWT_SECRET_KEY? (run python command)
- [ ] Have 4 required variables ready? (see above)
- [ ] Values exactly as shown? (especially `false` and `true` lowercase)
- [ ] JWT_SECRET_KEY is long string (64+ chars)?

✅ Yes? → Ready to add to Render!

---

## 📚 Need More Details?

- Full guide: [ENVIRONMENT_VARIABLES.md](ENVIRONMENT_VARIABLES.md)
- Setup walkthrough: [RENDER_QUICK_START.md](RENDER_QUICK_START.md)
- Complete reference: [RENDER_DETAILED_SETUP.md](RENDER_DETAILED_SETUP.md)

---

**Ready to deploy? 🚀 Go to Render and add these variables!**
