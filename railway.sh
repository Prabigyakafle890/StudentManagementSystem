#!/bin/bash

# Railway deployment script
echo "Starting deployment..."

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@edumanager.com', 'admin123')
    print('Admin user created')
else:
    print('Admin user already exists')
"

echo "Deployment complete!"