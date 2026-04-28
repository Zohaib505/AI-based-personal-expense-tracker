# ExpenseTracker - Frontend Architecture & Access Guide

## 🎯 Main Frontend Files

### **1. Base Templates**
- **base.html** - Main layout template (all pages extend this)
- **base_auth.html** - Authentication layout
- **navbar.html** - Navigation bar component
- **index.html** - Home/Dashboard page

### **2. Feature Templates**
```
templates/
├── authentication/     → Login, Register, Password Reset
├── expenses/          → Expense CRUD operations
├── income/            → Income tracking
├── goals/             → Savings goals
├── expense_forecast/  → 30-day predictions
├── preferences/       → User settings
├── userprofile/       → Profile management
└── partials/          → Reusable components
```

---

## 🚀 Access All Frontend Pages

### **Running Server**
```bash
# Terminal 1: Keep server running (already running!)
# Terminal 2: Test URLs
```

### **Main Entry Points**

| Feature | URL | File |
|---------|-----|------|
| **Home/Dashboard** | http://localhost:8000 | templates/index.html |
| **Expenses** | http://localhost:8000/expenses | templates/expenses/index.html |
| **Add Expense** | http://localhost:8000/add-expense | templates/expenses/add_expense.html |
| **Income** | http://localhost:8000/income | templates/income/income.html |
| **Goals** | http://localhost:8000/goals/list_goals/ | templates/goals/goals.html |
| **Forecast** | http://localhost:8000/forecast/ | templates/expense_forecast/index.html |
| **Reports** | http://localhost:8000/report | templates/report_generation/report.html |
| **Settings** | http://localhost:8000/preferences/preferences/ | templates/preferences/preferences.html |
| **Profile** | http://localhost:8000/account/profile/ | templates/userprofile/profile.html |
| **Admin Panel** | http://localhost:8000/admin | Django Admin |

---

## 🌐 Frontend Structure

### **Layout Hierarchy**
```
base.html (Main layout with navbar & sidebar)
├── index.html (Dashboard - extends base.html)
├── expenses/ (Expense pages - extend base.html)
│   ├── index.html (List expenses)
│   └── add_expense.html
├── income/ (Income pages)
│   └── income.html
├── goals/ (Goals pages)
│   └── goals.html
├── expense_forecast/ (Forecast)
│   └── index.html
└── report_generation/
    └── report.html
```

### **Static Files**
```
static/
├── css/
│   ├── bootstrap.min.css (Bootstrap framework)
│   ├── style.css (Main styling)
│   ├── dashboard.css (Dashboard specific)
│   ├── main.css (Additional styles)
│   └── sb-admin-2.min.css (Admin template)
├── js/
│   └── [JavaScript files]
└── img/
    └── [Images & icons]
```

---

## 📋 Complete URL Mapping

### **Expenses Module**
- `GET /` → Dashboard (index.html)
- `GET /expenses` → Expense list
- `GET /add-expense` → Add expense form
- `POST /add-expense` → Create expense
- `GET /edit-expense/<id>` → Edit form
- `POST /edit-expense/<id>` → Update expense
- `GET /expense-delete/<id>` → Delete expense
- `GET /search-expenses` → Search expenses
- `GET /expense_category_summary` → Category breakdown
- `GET /stats` → Statistics dashboard
- `GET /set-daily-expense-limit/` → Set daily limit

### **Authentication Module**
- `/authentication/register` → User registration
- `/authentication/login` → User login
- `/authentication/logout` → Logout
- `/authentication/password-reset` → Reset password
- `/authentication/activate/<token>` → Email verification

### **Income Module**
- `/income` → Income list
- `/income/add-income` → Add income
- `/income/edit/<id>` → Edit income
- `/income/delete/<id>` → Delete income
- `/income/export-pdf` → Export as PDF
- `/income/export-csv` → Export as CSV
- `/income/export-xlsx` → Export as Excel

### **Goals Module**
- `/goals/list_goals/` → List all goals
- `/goals/add-goal` → Create goal
- `/goals/add-goal-progress/<id>` → Add progress

### **Forecast Module**
- `/forecast/` → 30-day forecast

### **Reports Module**
- `/report` → Generate reports

### **User Settings**
- `/preferences/preferences/` → User preferences
- `/account/profile/` → User profile

---

## 🎨 Frontend Features

### **1. Dashboard (Home Page)**
- Real-time expense summary
- Category breakdown
- Recent transactions
- Quick action buttons

### **2. Expense Tracking**
- Add/Edit/Delete expenses
- Search & filter
- Category selection
- Date range selection

### **3. Income Tracking**
- Add income sources
- Track multiple income streams
- Export functionality

### **4. Expense Forecasting**
- 30-day prediction chart
- Trend analysis
- Visual graph

### **5. Goal Tracking**
- Set savings goals
- Track progress
- Milestone tracking

### **6. Reporting**
- PDF export
- CSV export
- Excel export
- Charts and graphs

---

## 🔐 User Authentication Flow

```
1. User visits http://localhost:8000
   ↓
2. Redirects to login if not authenticated
   ↓
3. User registers/logs in at /authentication/register or /authentication/login
   ↓
4. Session created, redirected to dashboard
   ↓
5. Can now access all features
```

---

## 📱 Main UI Components

### **Navigation Bar (navbar.html)**
- Logo/Home link
- User name display
- Logout button
- Active page highlight

### **Sidebar (in base.html)**
- Dashboard link
- Expenses link
- Income link
- Goals link
- Forecast link
- Reports link
- Settings link
- Profile link

### **Dashboard Cards**
- Total expenses
- Monthly average
- Expense by category
- Recent transactions

---

## 🚀 Quick Start for Frontend Testing

1. **Start Server** (Already Running):
   ```
   http://localhost:8000
   ```

2. **Access Dashboard**:
   - URL: http://localhost:8000
   - Shows home page or redirects to login

3. **Register/Login**:
   - Register: http://localhost:8000/authentication/register
   - Login: http://localhost:8000/authentication/login

4. **Add Test Data**:
   - Add Expense: http://localhost:8000/add-expense
   - Add Income: http://localhost:8000/income
   - Create Goal: http://localhost:8000/goals/list_goals/

5. **View Features**:
   - Dashboard: http://localhost:8000/expenses
   - Forecast: http://localhost:8000/forecast/
   - Reports: http://localhost:8000/report

---

## 🛠️ Frontend Technologies

- **HTML5** - Semantic markup
- **CSS3** - Styling with Bootstrap
- **JavaScript** - Interactivity
- **Bootstrap 4** - Responsive framework
- **Chart.js** - Data visualization
- **FontAwesome** - Icons
- **Django Templates** - Server-side rendering

---

## 📊 All URLs at a Glance

**Start here**: http://localhost:8000

**All Features**:
```
Home               → http://localhost:8000
Expenses           → http://localhost:8000/expenses
Add Expense        → http://localhost:8000/add-expense
Income             → http://localhost:8000/income
Goals              → http://localhost:8000/goals/list_goals/
Forecast           → http://localhost:8000/forecast/
Reports            → http://localhost:8000/report
Settings           → http://localhost:8000/preferences/preferences/
Profile            → http://localhost:8000/account/profile/
Admin              → http://localhost:8000/admin
```

---

## ✅ Current Server Status

- **Status**: ✅ Running
- **Address**: http://localhost:8000
- **Port**: 8000
- **Mode**: Persistent (Long-running)
- **Frontend**: Fully accessible
- **Database**: Connected & initialized

---

**Enjoy your ExpenseTracker application! 🎉**
