#!/bin/bash

# Exit on any error
set -e

# Function to check if MySQL is ready
wait_for_mysql() {
    echo "Waiting for MySQL database..."
    while ! mysql -h"${DB_HOST:-localhost}" -P"${DB_PORT:-3306}" -u"${DB_USER:-root}" -p"${DB_PASSWORD:-}" -e "SELECT 1" &> /dev/null; do
        echo "MySQL is unavailable - sleeping"
        sleep 2
    done
    echo "MySQL is up and running!"
}

# Function to run Django management commands
run_django_setup() {
    echo "Running Django setup..."
    
    # Run migrations
    echo "Running migrations..."
    python manage.py migrate --noinput
    
    # Collect static files
    echo "Collecting static files..."
    python manage.py collectstatic --noinput --clear
    
    # Create superuser if it doesn't exist
    if [ "${CREATE_SUPERUSER:-false}" = "true" ]; then
        echo "Creating superuser if needed..."
        python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
username = '${DJANGO_SUPERUSER_USERNAME:-admin}'
email = '${DJANGO_SUPERUSER_EMAIL:-admin@example.com}'
password = '${DJANGO_SUPERUSER_PASSWORD:-admin123}'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser created: {username}')
else:
    print(f'Superuser {username} already exists')
"
    fi
}

# Main execution
main() {
    echo "Starting messaging app container..."
    
    # Wait for database if configured
    if [ -n "${DB_HOST}" ]; then
        wait_for_mysql
    fi
    
    # Run Django setup
    run_django_setup
    
    # Check the command to run
    if [ "$1" = "runserver" ] || [ $# -eq 0 ]; then
        echo "Starting Django development server..."
        exec python manage.py runserver 0.0.0.0:8000
    elif [ "$1" = "gunicorn" ]; then
        echo "Starting Gunicorn server..."
        exec gunicorn messaging_app.wsgi:application \
            --bind 0.0.0.0:8000 \
            --workers 4 \
            --timeout 300 \
            --keep-alive 2 \
            --max-requests 1000 \
            --max-requests-jitter 100 \
            --log-level info
    elif [ "$1" = "bash" ] || [ "$1" = "sh" ]; then
        echo "Starting shell..."
        exec "$@"
    else
        echo "Executing command: $@"
        exec "$@"
    fi
}

# Run main function with all arguments
main "$@"