from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)

def handler404(request, exception=None):
    """Handle 404 errors"""
    logger.warning(f"404 error for path: {request.path} by user: {request.user}")
    return render(request, '404.html', status=404)

def handler500(request):
    """Handle 500 errors"""
    logger.error(f"500 error for user: {request.user}")
    return render(request, '500.html', status=500)
