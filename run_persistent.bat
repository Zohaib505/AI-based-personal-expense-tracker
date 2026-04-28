@echo off
REM ExpenseTracker - Production-Ready Local Server
REM This will keep running indefinitely

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     ExpenseTracker - Local Development Server             ║
echo ║     Running in Persistent Mode (Long-Duration)            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Navigate to project directory
cd /d "C:\Users\jk\Documents\dead final FYP\Expensetracker-master"

REM Activate conda environment
call conda activate fyp

if errorlevel 1 (
    echo ERROR: Could not activate conda environment 'fyp'
    pause
    exit /b 1
)

echo ✓ Environment activated
echo.

REM Check if database exists, if not create it
if not exist "db.sqlite3" (
    echo Creating database...
    python manage.py migrate
    echo.
    echo Database created!
    echo.
)

echo.
echo ════════════════════════════════════════════════════════════
echo Starting Persistent Development Server
echo ════════════════════════════════════════════════════════════
echo.
echo 📱 Application URL:     http://localhost:8000
echo 🔐 Admin Panel:         http://localhost:8000/admin
echo 📊 Dashboard:           http://localhost:8000/expenses
echo 📈 Forecast:            http://localhost:8000/forecast/
echo 🎯 Goals:               http://localhost:8000/goals/list_goals/
echo 💰 Income:              http://localhost:8000/income
echo 📄 Reports:             http://localhost:8000/report
echo.
echo This server will run continuously.
echo To stop: Press CTRL+C
echo.
echo ════════════════════════════════════════════════════════════
echo.

REM Run in persistent mode with autoreload
python manage.py runserver 0.0.0.0:8000

REM If server stops, offer to restart
pause
goto :start
:start
call conda activate fyp
python manage.py runserver 0.0.0.0:8000
goto :start
