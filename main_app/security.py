"""
Security configuration and utilities for the college management system.
"""

from django.conf import settings
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
import logging

logger = logging.getLogger(__name__)

# User role constants
class UserRoles:
    ADMIN = '1'
    STAFF = '2'
    STUDENT = '3'

# Security configuration
SECURITY_CONFIG = {
    'MAX_LOGIN_ATTEMPTS': 5,
    'LOGIN_LOCKOUT_TIME': 300,  # 5 minutes
    'SESSION_TIMEOUT': 3600,    # 1 hour
    'CSRF_COOKIE_AGE': 3600,
    'PASSWORD_MIN_LENGTH': 8,
    'REQUIRE_HTTPS': not settings.DEBUG,
}

def log_security_event(event_type, user, details=None):
    """
    Log security-related events for monitoring.
    """
    logger.warning(f"Security Event: {event_type} - User: {user} - Details: {details}")

def check_user_permissions(user, required_role=None):
    """
    Check if user has required permissions.
    """
    if not user.is_authenticated:
        raise PermissionDenied("Authentication required")
    
    if required_role and user.user_type != required_role:
        log_security_event("UNAUTHORIZED_ACCESS", user, f"Required role: {required_role}")
        raise PermissionDenied("Insufficient permissions")
    
    return True

def sanitize_input(data):
    """
    Basic input sanitization to prevent XSS and injection attacks.
    """
    if isinstance(data, str):
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', 'script', 'javascript']
        for char in dangerous_chars:
            data = data.replace(char, '')
    
    return data

def validate_file_upload(uploaded_file):
    """
    Validate uploaded files for security.
    """
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx']
    max_file_size = 5 * 1024 * 1024  # 5MB
    
    if uploaded_file.size > max_file_size:
        raise ValueError("File size too large")
    
    file_extension = uploaded_file.name.lower().split('.')[-1]
    if f'.{file_extension}' not in allowed_extensions:
        raise ValueError("File type not allowed")
    
    return True
