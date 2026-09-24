# =========================================================
# MOOMEEN PRODUCTS - Cloud Run Production Dockerfile
# Python 3.12 Slim + Gunicorn + PostgreSQL + Static Assets
# =========================================================

FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Install system dependencies required for PostgreSQL (psycopg) and Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django application source code
COPY backend/ ./

# Run collectstatic during build (using build-time environment flags)
ENV DJANGO_SECRET_KEY=build-time-insecure-secret-key-for-collectstatic \
    DJANGO_DEBUG=true

RUN python manage.py collectstatic --noinput

# Inform Docker that Cloud Run routes traffic to PORT 8080
EXPOSE 8080

# Start Gunicorn with workers and threads optimized for Cloud Run container instances
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 moomeen.wsgi:application
