# ExpenseTracker - Server Setup Guide (Final Year Project)

## ⚡ Quick Start - Server Setup (2 minutes)

### 🔴 Step 1: Apply Database Migrations

```powershell
conda activate fyp
cd "c:\Users\jk\Documents\dead final FYP\Expensetracker-master"
python manage.py migrate
```

**This will:**
- Create all database tables
- Set up voice_feature module
- Initialize the database schema

### 🟢 Step 2: Start the Development Server

**Option A: Using Batch File (Easiest)**
```batch
Double-click: start_server.bat
```

**Option B: Using PowerShell**
```powershell
conda activate fyp
cd "c:\Users\jk\Documents\dead final FYP\Expensetracker-master"
python manage.py runserver
```

### ✅ Expected Output

When the server starts successfully, you should see:
```
System check identified no issues (0 silenced).
Django version 5.1.1, using settings 'expensetracker.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**Server is now running at**: http://127.0.0.1:8000 ✅

---

## 🔐 Login Credentials

```
Username: hammad123
Password: malik5633
```

---

## � Troubleshooting

### Issue: Port 8000 In Use
```powershell
python manage.py runserver 8080
```

### Issue: Module Not Found
```powershell
pip install -r requirements.txt
```

### Issue: Database Locked
```powershell
del mydatabase
python manage.py migrate
```

### Issue: Static Files Missing
```powershell
python manage.py collectstatic --noinput
```

### Issue: AttributeError or Import Errors
```powershell
python manage.py check
```

---

## ✅ Server Setup Complete!

Your Intelligent Expense Tracker is now ready to run. Access it at: **http://127.0.0.1:8000/**

Good luck with your FYP defense! 🎓