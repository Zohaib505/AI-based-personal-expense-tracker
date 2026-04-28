@echo off
cd /d "C:\Users\jk\Documents\FYP more strong option\Expensetracker-master"
call conda activate fyp
python manage.py runserver 0.0.0.0:8000
pause
