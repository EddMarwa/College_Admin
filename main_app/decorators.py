"""
Security decorators for the college management system.
These decorators provide secure alternatives to @csrf_exempt.
"""

from functools import wraps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
import json


def ajax_login_required(view_func):
    """
    Decorator that requires authentication for AJAX requests.
    Returns JSON error response if user is not authenticated.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'error',
                'message': 'Authentication required'
            }, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def role_required(*allowed_roles):
    """
    Decorator that checks if user has required role.
    Usage: @role_required('1', '2') for admin and staff
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Authentication required'
                }, status=401)
            
            if request.user.user_type not in allowed_roles:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Insufficient permissions'
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def secure_ajax_view(allowed_methods=None, allowed_roles=None):
    """
    Secure decorator for AJAX views that combines multiple security checks.
    
    Args:
        allowed_methods: List of allowed HTTP methods (e.g., ['POST', 'GET'])
        allowed_roles: List of allowed user roles (e.g., ['1', '2'])
    """
    if allowed_methods is None:
        allowed_methods = ['POST']
    
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check HTTP method
            if request.method not in allowed_methods:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Method {request.method} not allowed'
                }, status=405)
            
            # Check authentication
            if not request.user.is_authenticated:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Authentication required'
                }, status=401)
            
            # Check user role if specified
            if allowed_roles and request.user.user_type not in allowed_roles:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Insufficient permissions'
                }, status=403)
            
            # Check if request is AJAX for certain endpoints
            if request.method == 'POST' and not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Allow form submissions but log them
                pass
            
            return view_func(request, *args, **kwargs)
        
        return _wrapped_view
    return decorator


def validate_json_request(view_func):
    """
    Decorator that validates JSON request data.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                request.json = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid JSON data'
                }, status=400)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
