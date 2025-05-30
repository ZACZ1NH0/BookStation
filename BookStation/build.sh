#!/bin/bash

# Cài thư viện
pip install -r BookStation/requirements.txt

# Chạy migrate
python BookStation/manage.py migrate

# Tạo superuser nếu chưa có
echo "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'soloyasuokom@gmail.com', '1234')
    print('Superuser created.')
else:
    print('Superuser already exists.')
" | python manage.py shell
