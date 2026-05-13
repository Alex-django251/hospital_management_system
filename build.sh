#!/usr/bin/env bash
set -e

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput

python manage.py shell << 'EOF'
from users.models import User
try:
    u = User.objects.get(username='admin')
    u.set_password('yourpassword123')
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print('Password reset successfully!')
except User.DoesNotExist:
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='yourpassword123'
    )
    print('Superuser created!')
EOF
