release: python manage.py migrate
web: waitress-serve --listen=127.0.0.1:8000 storefront.wsgi:application
worker: celery -A storefront worker
