import os
import traceback
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensetracker.settings')
import django
django.setup()
from django.test import Client
from django.contrib.auth.models import User

c = Client()
u = User.objects.get(username='hammad123')
c.force_login(u)

try:
    r = c.get('/add-expense/')
    print('STATUS', r.status_code)
    print(r.content[:1000])
except Exception:
    traceback.print_exc()
