@echo off
REM ExpenseTracker - Local Development Startup Script

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     ExpenseTracker - Local Development Server             ║
echo ║     Final Year Project                                    ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Activate conda environment
echo Activating conda environment 'fyp'...
call conda activate fyp

if errorlevel 1 (
    echo.
    echo ERROR: Could not activate conda environment 'fyp'
    echo Make sure you have Anaconda installed and created the 'fyp' environment
    echo.
    pause
    exit /b 1
)

echo ✓ Environment activated
echo.

REM Check if database exists
if not exist "mydatabase" (
    echo Database not found. Creating new database...
    python manage.py migrate
    echo.
    echo Database created!
    echo.
    echo Now create a superuser for admin access:
    echo.
    python manage.py createsuperuser
    echo.
)

echo.
echo ════════════════════════════════════════════════════════════
echo Starting Development Server...
echo ════════════════════════════════════════════════════════════
echo.
echo 📱 Application URL:     http://localhost:8000
echo 🔐 Admin Panel:         http://localhost:8000/admin
echo 📊 Dashboard:           http://localhost:8000/expenses
echo.
echo To stop the server: Press CTRL+C
echo.
echo ════════════════════════════════════════════════════════════
echo.

REM Run development server
python manage.py runserver

pause
