from django.http import JsonResponse
from django.utils import timezone
from django.db import connection
from django.conf import settings
import sys


def health_check(request):
    """
    Health check endpoint for container monitoring and load balancers.
    Returns service status, database connectivity, and basic system info.
    """
    status = "healthy"
    checks = {}
    
    # Database connectivity check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"
        status = "unhealthy"
    
    # Basic system checks
    checks.update({
        "python_version": sys.version.split()[0],
        "django_version": settings.DJANGO_VERSION if hasattr(settings, 'DJANGO_VERSION') else "unknown",
        "timestamp": timezone.now().isoformat(),
        "debug_mode": settings.DEBUG,
    })
    
    response_data = {
        "status": status,
        "service": "messaging-app",
        "version": "1.0.0",
        "checks": checks
    }
    
    # Return appropriate HTTP status code
    status_code = 200 if status == "healthy" else 503
    
    return JsonResponse(response_data, status=status_code)


def readiness_check(request):
    """
    Readiness check for Kubernetes and container orchestrators.
    Checks if the service is ready to handle requests.
    """
    ready = True
    checks = {}
    
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            checks["database"] = "ready"
    except Exception as e:
        checks["database"] = f"not ready: {str(e)}"
        ready = False
    
    # Add more readiness checks as needed
    # - Check external service dependencies
    # - Check required configuration
    # - Check file system access
    
    response_data = {
        "ready": ready,
        "service": "messaging-app",
        "checks": checks,
        "timestamp": timezone.now().isoformat()
    }
    
    status_code = 200 if ready else 503
    return JsonResponse(response_data, status=status_code)


def liveness_check(request):
    """
    Liveness check for Kubernetes and container orchestrators.
    Simple check to verify the service is alive.
    """
    return JsonResponse({
        "alive": True,
        "service": "messaging-app",
        "timestamp": timezone.now().isoformat()
    })
