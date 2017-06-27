#!/bin/bash

USERNAME="admin"
EMAIL="admin@example.com"
PASSWORD="@ECSE428"

# Migrate database
./update_db.sh

# Create super user
echo "Creating Super User..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$USERNAME', '$EMAIL', '$PASSWORD')" | python3 movie_explorer/manage.py shell &> /dev/null 2>&1

echo "DONE"