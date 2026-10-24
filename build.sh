#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# Create the admin user on the free plan (no Shell). Set DJANGO_SUPERUSER_EMAIL,
# DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD in Render's Environment tab.
if [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
  python manage.py createsuperuser --noinput || echo "Superuser already exists, skipping."
fi
