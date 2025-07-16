# Security Setup Guide

This guide outlines the security measures implemented in the College Management System.

## Environment Setup

1. **Create Environment File**:
   ```bash
   cp .env.example .env
   ```

2. **Configure Environment Variables**:
   Edit `.env` file with your secure values:
   ```
   SECRET_KEY=your-super-secret-key-here-min-50-chars
   DEBUG=False
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   EMAIL_ADDRESS=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   ```

3. **Generate Secret Key**:
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

## Security Features Implemented

### 1. Environment Variables
- Sensitive data moved to environment variables
- `.env` file excluded from git
- Example configuration provided

### 2. CSRF Protection
- Custom secure decorators replace `@csrf_exempt`
- Role-based access control
- AJAX request validation

### 3. Security Headers
- XSS protection enabled
- Content type sniffing protection
- Clickjacking protection
- HSTS headers for HTTPS

### 4. Session Security
- Secure session cookies
- Session timeout (1 hour)
- Session expiry on browser close

### 5. Input Validation
- File upload restrictions
- Input sanitization
- JSON request validation

### 6. Authentication & Authorization
- Role-based access control
- Login required decorators
- Permission checking utilities

## Before Deployment

### 1. Update Settings for Production
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 2. Database Security
- Use strong database passwords
- Enable database SSL connections
- Regular database backups

### 3. Server Security
- Use HTTPS/SSL certificates
- Configure firewall rules
- Regular security updates
- Monitor logs for suspicious activity

## Security Checklist

- [ ] Environment variables configured
- [ ] Secret key changed from default
- [ ] DEBUG set to False in production
- [ ] HTTPS enabled
- [ ] Database credentials secured
- [ ] File upload restrictions in place
- [ ] Security headers configured
- [ ] Session security enabled
- [ ] Input validation implemented
- [ ] Logging configured for security events

## Monitoring

- Check Django logs for security events
- Monitor failed login attempts
- Review file upload activities
- Track unauthorized access attempts

## Emergency Response

If security breach suspected:
1. Immediately change all passwords
2. Revoke and regenerate secret keys
3. Review access logs
4. Update and patch all systems
5. Notify relevant stakeholders
