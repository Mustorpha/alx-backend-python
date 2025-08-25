# Use Python 3.10 slim image for smaller size
FROM python:3.10-slim

# Build arguments
ARG BUILDTIME
ARG VERSION
ARG REVISION

# Set labels for better image metadata
LABEL org.opencontainers.image.created="${BUILDTIME}"
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.revision="${REVISION}"
LABEL org.opencontainers.image.title="Messaging App"
LABEL org.opencontainers.image.description="Django messaging application"
LABEL org.opencontainers.image.source="https://github.com/Mustorpha/alx-backend-python"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=messaging_app.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    default-mysql-client \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user early
RUN adduser --disabled-password --gecos '' appuser

# Copy requirements file first for better layer caching
COPY Requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r Requirements.txt

# Copy entrypoint script
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Copy project files
COPY . /app/

# Create directory for static files and set permissions
RUN mkdir -p /app/staticfiles \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health/', timeout=10)" || exit 1

# Expose port 8000
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]