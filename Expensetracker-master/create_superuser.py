import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensetracker.settings')
django.setup()

User = get_user_model()

# Create superuser if it doesn't exist
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✓ Superuser '{username}' created successfully!")
    print(f"  Username: {username}")
    print(f"  Email: {email}")
    print(f"  Password: {password}")
else:
    print(f"✓ Superuser '{username}' already exists!")
