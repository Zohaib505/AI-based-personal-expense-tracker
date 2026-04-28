# ExpenseTracker - Local Setup Guide (Final Year Project)

## Quick Start (5 minutes)

### Step 1: Activate Environment
```bash
conda activate fyp
```

### Step 2: Navigate to Project
```bash
cd "c:\Users\jk\Documents\dead final FYP\Expensetracker-master"
```

### Step 3: Run Development Server
```bash
python manage.py runserver
```

### Step 4: Access Application
- **Open Browser**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API**: http://localhost:8000/api/predict-category/

---

## Detailed Local Setup

### 1. Database Setup

The project uses SQLite by default (database already exists: `mydatabase`)

**To reset database (start fresh):**
```bash
# Delete old database
del mydatabase

# Create new database with migrations
python manage.py migrate
```

### 2. Create Admin User (Superuser)

```bash
python manage.py createsuperuser
```

**Example:**
- Username: `admin`
- Email: `admin@localhost.com`
- Password: `admin123`

### 3. Run Development Server

```bash
python manage.py runserver
```

**Output should show:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 4. Access Application

| Feature | URL |
|---------|-----|
| Dashboard | http://localhost:8000/expenses/ |
| Admin | http://localhost:8000/admin/ |
| Login | http://localhost:8000/authentication/login/ |
| Register | http://localhost:8000/authentication/register/ |

---

## First Time Setup (Complete)

### Step 1: Install Dependencies (If Not Done)
```bash
conda activate fyp
pip install -r requirements.txt
pip install django-environ python-dotenv
```

### Step 2: Create .env File for Local Development
```bash
# Copy the example
copy .env.example .env
```

**Edit `.env` for local use:**
```env
DEBUG=True
SECRET_KEY=django-insecure-local-development-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=mydatabase
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Step 3: Apply Migrations
```bash
python manage.py migrate
```

### Step 4: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 5: Load Sample Data (Optional)
```bash
python manage.py loaddata initial_data.json
```

### Step 6: Run Server
```bash
python manage.py runserver
```

---

## Testing the Application Locally

### 1. Create a Test User
- Go to http://localhost:8000/authentication/register/
- Register with:
  - Email: `test@example.com`
  - Password: `testpass123`

### 2. Add Test Data

#### Add Income Source
1. Login
2. Go to Account → Income Sources
3. Add source (e.g., "Salary", "Freelance")

#### Add Income
1. Dashboard → Income
2. Click "Add Income"
3. Fill form:
   - Amount: 50000
   - Source: Choose from dropdown
   - Description: "Monthly salary"
   - Date: Select date

#### Add Expense Category (If Needed)
1. Go to Admin Panel (http://localhost:8000/admin/)
2. Navigate to Expenses → Categories
3. Add categories (e.g., "Food", "Transport", "Entertainment")

#### Add Expense
1. Dashboard → Expenses
2. Click "Add Expense"
3. Fill form:
   - Amount: 500
   - Category: Choose
   - Description: "Lunch"
   - Date: Select date

### 3. View Reports
- Dashboard → Reports
- Select date range
- View summaries
- Export to PDF/CSV/Excel

### 4. Test Forecasting
- Dashboard → Forecast
- View 30-day expense prediction

---

## Useful Development Commands

### Check Everything is OK
```bash
python manage.py check
```

### Create Backup of Database
```bash
# Backup
python manage.py dumpdata > backup.json

# Restore
python manage.py loaddata backup.json
```

### Access Database Shell
```bash
python manage.py dbshell
```

### Access Python Shell
```bash
python manage.py shell

# Example: Create test user
>>> from django.contrib.auth.models import User
>>> User.objects.create_user('testuser', 'test@example.com', 'password123')
>>> exit()
```

### View Database Migrations
```bash
python manage.py showmigrations
```

### Reset Everything (Start Fresh)
```bash
# Delete database
del mydatabase

# Recreate database
python manage.py migrate

# Create new admin user
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

## Accessing Different Parts of Application

### User Features

| Feature | Path | URL |
|---------|------|-----|
| Dashboard | Dashboard link | http://localhost:8000/expenses/ |
| Add Expense | Dashboard → Add Expense | http://localhost:8000/expenses/add-expense/ |
| View Expenses | Dashboard → Expenses | http://localhost:8000/expenses/ |
| Income | Navigation → Income | http://localhost:8000/income/ |
| Goals | Navigation → Goals | http://localhost:8000/goals/ |
| Reports | Navigation → Reports | http://localhost:8000/income/report/ |
| Forecast | Navigation → Forecast | http://localhost:8000/forecast/ |
| Settings | Navigation → Preferences | http://localhost:8000/preferences/ |

### Admin Panel

**URL**: http://localhost:8000/admin/

**Login with superuser credentials created earlier**

Available:
- User management
- Expense categories
- Income sources
- User preferences
- All data viewing

---

## For Project Demonstration

### Demonstrate Key Features

**1. User Registration & Login**
- Show registration form
- Show login process
- Show user dashboard

**2. Expense Tracking**
- Add multiple expenses
- Show categorization
- Show expense list

**3. Income Tracking**
- Add income entries
- Show income dashboard
- View income summary

**4. Reports & Analytics**
- Show daily/weekly/monthly summaries
- Export to PDF
- Export to Excel
- Show charts/statistics

**5. Forecasting**
- Show 30-day forecast
- Explain ARIMA model

**6. ML Category Prediction**
- Add expense with description
- Show automatic category prediction
- Explain model training

**7. Admin Panel**
- Show user management
- Show data management
- Show logs

---

## Troubleshooting Local Setup

### Issue: "ModuleNotFoundError: No module named 'django'"

**Solution:**
```bash
conda activate fyp
pip install django==5.1.1
pip install -r requirements.txt
```

### Issue: Database "mydatabase" locked

**Solution:**
```bash
# Close any Django shells or servers
# Delete database and recreate
del mydatabase
python manage.py migrate
```

### Issue: Port 8000 already in use

**Solution:**
```bash
# Use different port
python manage.py runserver 8080

# Then access: http://localhost:8080
```

### Issue: Static files not loading (CSS/images missing)

**Solution:**
```bash
python manage.py collectstatic --noinput
```

### Issue: Email not sending (but appearing in console)

**This is normal for local development!** Emails print to console instead of sending.

To see sent emails:
```
Check the terminal where runserver is running - emails appear there
```

### Issue: Forecast not working

**Solution:**
```bash
# Need at least 10 expenses to forecast
python manage.py shell
>>> from expenses.models import Expense
>>> Expense.objects.count()  # Should be >= 10
```

---

## Quick Reference - Common Tasks

### Change Admin Password
```bash
python manage.py changepassword admin
```

### Create Another Superuser
```bash
python manage.py createsuperuser
```

### Delete All User Data (Keep Structure)
```bash
python manage.py shell
>>> from expenses.models import Expense
>>> from userincome.models import UserIncome
>>> Expense.objects.all().delete()
>>> UserIncome.objects.all().delete()
>>> exit()
```

### Add Test Categories
```bash
python manage.py shell
>>> from expenses.models import Category
>>> categories = ['Food', 'Transport', 'Entertainment', 'Utilities', 'Healthcare', 'Shopping']
>>> for cat in categories:
>>>     Category.objects.create(name=cat)
>>> exit()
```

### Check Database Size
```bash
# In PowerShell
Get-Item mydatabase | Select-Object -ExpandProperty Length
```

---

## Environment Variables for Local Development

Your `.env` file for local development:

```env
# Local Development Settings
DEBUG=True
SECRET_KEY=django-insecure-development-key-not-secure
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database - SQLite (Local)
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=mydatabase

# Email - Console Backend (prints to terminal)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Celery - Local Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Security - Disabled for Local
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

---

## Testing All Features Checklist

✅ **Authentication**
- [ ] Register new user
- [ ] Login with credentials
- [ ] Logout successfully
- [ ] Password reset flow

✅ **Expense Tracking**
- [ ] Add expense
- [ ] View expenses
- [ ] Edit expense
- [ ] Delete expense
- [ ] Search expenses
- [ ] Filter by category

✅ **Income Tracking**
- [ ] Add income source
- [ ] Add income
- [ ] View income
- [ ] Edit income
- [ ] Delete income

✅ **Goals**
- [ ] Create savings goal
- [ ] Add amount to goal
- [ ] Complete goal
- [ ] View goal progress

✅ **Reports**
- [ ] View daily summary
- [ ] View weekly summary
- [ ] View monthly summary
- [ ] Export to PDF
- [ ] Export to CSV
- [ ] Export to Excel

✅ **Forecasting**
- [ ] View expense forecast
- [ ] Check prediction accuracy

✅ **Admin Panel**
- [ ] Login to admin
- [ ] View users
- [ ] View expenses
- [ ] View income
- [ ] Create new category

---

## Performance Notes (Local)

Since you're running locally:
- **ML Model Training**: First prediction takes ~2-3 seconds (normal - model training)
- **Subsequent Predictions**: < 500ms
- **Forecast Generation**: 5-10 seconds (ARIMA fitting)
- **Reports**: 1-2 seconds (data aggregation)

This is **expected behavior** locally with SQLite database.

---

## Tips for Final Year Project

### Presentation Tips
1. **Start Fresh**: Delete old database, create new one
2. **Pre-populate Data**: Add test data before demo
3. **Multiple Users**: Show multi-user capabilities
4. **Error Handling**: Try invalid inputs to show validation
5. **Performance**: Mention improvements for production

### What to Highlight
- Multi-user expense tracking system
- ML-powered category prediction
- 30-day ARIMA forecasting
- Comprehensive reporting
- Data export functionality
- Security & authentication
- Error handling & validation
- Responsive UI

### Code to Show Examiners
- Django models (multi-tenant design)
- API endpoints (DRF implementation)
- ML model integration (scikit-learn)
- View functions (business logic)
- Error handling (production-ready)

---

## Summary

**To run locally:**
1. `conda activate fyp`
2. `python manage.py runserver`
3. Open http://localhost:8000

**That's it! Your project is running locally.**

For detailed features and testing, follow the sections above.

Good luck with your Final Year Project! 🎓
