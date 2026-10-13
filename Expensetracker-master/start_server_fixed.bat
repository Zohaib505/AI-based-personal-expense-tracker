@echo off
REM =============================================
REM Expense Tracker - Run Server with Auto-Migrate
REM =============================================

echo.
echo ===================================
echo  Expense Tracker - Django Server
echo ===================================
echo.

REM Get the directory of this script
cd /d "%~dp0"

echo Activating conda environment (fyp)...
call conda activate fyp

echo.
echo Applying database migrations (one-time setup)...
echo.

python manage.py migrate

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Migrations failed!
    pause
    exit /b 1
)

echo.
echo ===================================
echo  Migrations Complete!
echo ===================================
echo.
echo Starting Django development server...
echo.
echo Access at: http://127.0.0.1:8000
echo.
echo Demo User:
echo   Username: hammad123
echo   Password: malik5633
echo.
echo To stop server: Press Ctrl+Break
echo.
echo ===================================
echo.

python manage.py runserver

REM This runs indefinitely until user presses Ctrl+Break
