@echo off
REM Run Django server with error output
cd /d "C:\Users\jk\Documents\FYP more strong option\Expensetracker-master"
echo Starting Django server...
echo.

call conda activate fyp

REM Run system check first
echo Running Django system checks...
python manage.py check

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: System checks failed!
    echo Please check the errors above.
    pause
    exit /b 1
)

echo.
echo System checks passed!
echo Starting server on 0.0.0.0:8000
echo.

REM Run the server
python manage.py runserver 0.0.0.0:8000

pause
