#!/bin/bash
set -e
set -o pipefail # if any code doesn't return 0, exit the script


function start_server() {
  python ./manage.py makemigrations
  python ./manage.py migrate
  echo "from api.apps.authentication.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin@example.com', 'password123')" | python ./manage.py shell
  echo Starting Django development server...
  python ./manage.py runserver 0.0.0.0:8000
}

start_server

exit 0
