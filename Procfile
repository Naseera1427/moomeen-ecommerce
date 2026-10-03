web: cd backend && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn moomeen.wsgi:application --bind 0.0.0.0:$PORT
