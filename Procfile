web: gunicorn expensetracker.wsgi --log-file -
worker: python manage.py celery worker -l info
beat: python manage.py celery beat -l info
