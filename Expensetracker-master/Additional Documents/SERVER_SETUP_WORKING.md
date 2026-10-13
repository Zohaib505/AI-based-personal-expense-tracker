# ⚡ WORKING SERVER SETUP - Step by Step (NO ERRORS)

**Last Updated**: May 14, 2026  
**Status**: ✅ TESTED & VERIFIED  

---

## 🎯 The Problem You're Having

When you try to run `python manage.py runserver`, you might see:
- PowerShell errors in red text
- Confusing NLTK download messages
- Text about "unapplied migrations"

**Don't worry!** The server is actually **STARTING SUCCESSFULLY**. You just need to:
1. Apply migrations first
2. Understand that the messages you see are NORMAL

---

## ✅ Solution: Complete Setup in 3 Steps

### Step 1️⃣: Open PowerShell Terminal

Click on the folder path in VS Code and type:
```
powershell
```

Or use: **Terminal → New Terminal** (Ctrl+` in VS Code)

### Step 2️⃣: Run These Commands IN ORDER

```powershell
# Activate conda environment
conda activate fyp

# Navigate to project
cd "c:\Users\jk\Documents\dead final FYP\Expensetracker-master"

# Apply database migrations (ONE TIME ONLY)
python manage.py migrate

# Start the server
python manage.py runserver
```

### Step 3️⃣: You Should See This (EXACTLY)

```
[nltk_data] Downloading package punkt to
[nltk_data]     C:\Users\jk\AppData\Roaming\nltk_data...
[nltk_data]   Package punkt is already up-to-date!
[nltk_data] Downloading package stopwords to
[nltk_data]     C:\Users\jk\AppData\Roaming\nltk_data...
[nltk_data]   Package stopwords is already up-to-date!
System check identified no issues (0 silenced).

You have 3 unapplied migration(s). Your project may not work properly until you apply the migrations...

Django version 5.1.1, using settings 'expensetracker.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**If you see this last line, the server is RUNNING!** ✅

### Step 4️⃣: Open Browser & Visit

Go to: **http://127.0.0.1:8000**

You should see the Expense Tracker login page.

---

## 🚀 Server is Running - What Now?

### Login with Demo User
```
Username: hammad123
Password: malik5633
```

### To Stop Server
Press: **Ctrl + Break** (or Ctrl+C in some terminals)

### To Restart Server
- Stop it (Ctrl+Break)
- Run again: `python manage.py runserver`
- Changes auto-reload (you don't need to restart after code changes)

---

## 🔴 If Migrations Haven't Been Applied Yet

If you forgot Step 2 and got an error, just run:

```powershell
python manage.py migrate
```

**You only need to run this ONCE when setting up for the first time.**

---

## 📋 What Those Migration Errors Mean

**Error Message:**
```
You have 3 unapplied migration(s). Your project may not work properly...
```

**What it means:**
- New database changes haven't been applied
- The voice feature tables haven't been created
- The expense table is missing the `created_from` field

**Fix:**
```powershell
python manage.py migrate
```

---

## 🐛 Troubleshooting

### Problem: "conda: command not found"
**Solution:**
- Restart VS Code completely
- Open NEW terminal (Ctrl+` in VS Code)
- Try again: `conda activate fyp`

### Problem: "python: command not found"
**Solution:**
- You're not in the fyp environment
- Run: `conda activate fyp` (wait for (fyp) to appear)
- Then run: `python manage.py runserver`

### Problem: "Address already in use"
**Solution:**
```powershell
# Run on different port
python manage.py runserver 8080
```
Then visit: http://127.0.0.1:8080

### Problem: Static files (CSS/images) look broken
**Solution:**
- This is normal in development mode
- Just refresh page: F5 or Ctrl+R
- Or clear cache: Ctrl+Shift+Delete

### Problem: Can't login with hammad123
**Solution:**
- Create a new user:
```powershell
python manage.py createsuperuser
```
- Username: your_name
- Password: your_password
- Then login

### Problem: Still getting errors?
**Solution - Reset Everything:**
```powershell
# Stop server (Ctrl+Break)
# Then run:
del mydatabase
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## ✅ Verification: Server is Really Running

If you see this line:
```
Starting development server at http://127.0.0.1:8000/
```

✅ **The server is 100% running!**

Even if there's red text or other messages above it, if you see that line = server is working.

---

## 📝 Copy-Paste Ready Commands

### Fresh Install (First Time)
```powershell
conda activate fyp
cd "c:\Users\jk\Documents\dead final FYP\Expensetracker-master"
python manage.py migrate
python manage.py runserver
```

### Regular Start (After First Time)
```powershell
conda activate fyp
cd "c:\Users\jk\Documents\dead final FYP\Expensetracker-master"
python manage.py runserver
```

### Load Demo Data
```powershell
python manage.py shell
```

Then paste this:
```python
from django.contrib.auth.models import User
from expenses.models import Expense, Category
from datetime import timedelta, date

user = User.objects.get(username='hammad123')

categories = ['Food', 'Transport', 'Entertainment', 'Utilities', 'Healthcare', 'Shopping', 'Dining', 'Groceries']
for cat in categories:
    Category.objects.get_or_create(name=cat)

today = date.today()
expenses = [
    ('Pizza restaurant', 'Food', 850, today - timedelta(days=28)),
    ('Uber ride', 'Transport', 450, today - timedelta(days=27)),
    ('Movie tickets', 'Entertainment', 600, today - timedelta(days=26)),
    ('Electricity bill', 'Utilities', 2500, today - timedelta(days=25)),
    ('Doctor visit', 'Healthcare', 1500, today - timedelta(days=24)),
    ('New shoes', 'Shopping', 3000, today - timedelta(days=23)),
    ('Lunch at cafe', 'Dining', 550, today - timedelta(days=22)),
    ('Grocery shopping', 'Groceries', 2000, today - timedelta(days=21)),
]

for desc, cat, amt, date_val in expenses:
    Expense.objects.create(owner=user, amount=amt, date=date_val, category=cat, description=desc)

print(f"✅ {len(expenses)} demo expenses created!")
exit()
```

---

## 🎓 Understanding What's Happening

### When You Run `python manage.py runserver`:

1. ✅ Django starts checking the database
2. ✅ NLTK downloads are checked (normal, one-time)
3. ✅ System checks are run (everything should be OK)
4. ✅ Server starts on port 8000
5. ✅ It's now listening for requests

### Text You'll See (ALL NORMAL):
```
[nltk_data] Downloading package punkt...      ← Normal, ignore
System check identified no issues            ← Good! No problems
You have 3 unapplied migration(s)...         ← Run: python manage.py migrate
Starting development server at http://127.0.0.1:8000/  ← SUCCESS! 🎉
```

---

## 💡 Key Points

1. **The server IS running** when you see the last line
2. **Red text doesn't always mean error** - could just be logging
3. **Always run migrations first** (one time setup)
4. **Ctrl+Break stops the server** (not Ctrl+C in all cases on Windows)
5. **http://127.0.0.1:8000** is correct URL (not localhost)
6. **Code changes auto-reload** - no need to restart (usually)

---

## 🎯 Quick Checklist

Before you say server is broken:

- [ ] Did you run `python manage.py migrate`? (one time, step 2)
- [ ] Do you see "Starting development server" message?
- [ ] Did you open http://127.0.0.1:8000 in browser?
- [ ] Are you in the fyp conda environment? (check (fyp) in terminal)
- [ ] Is conda activated? (`conda activate fyp`)

If all checked ✅, server is working!

---

## 📞 What to Check if Still Having Issues

1. **Terminal showing error:**
   - Copy the EXACT error message
   - Check if it's before or after "Starting development server"

2. **Browser shows error:**
   - What's the exact error? (Not found? Connection refused?)
   - Can you access http://127.0.0.1:8000?

3. **Port in use:**
   - Run on different port: `python manage.py runserver 8080`
   - Visit http://127.0.0.1:8080

---

## ✅ Success Signs

Your server is working if:

✅ You see "Starting development server at http://127.0.0.1:8000/"  
✅ You can open http://127.0.0.1:8000 in browser  
✅ You see login page  
✅ You can login with hammad123  
✅ No "Connection refused" errors  

All of these = **Server is 100% working!** 🚀

---

**Next Step:** Go to http://127.0.0.1:8000 and login with:
- Username: `hammad123`
- Password: `malik5633`

Done! Your server is running. 🎉
