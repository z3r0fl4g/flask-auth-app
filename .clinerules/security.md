# Security Rules

## Authentication

- All password handling must use Werkzeug security helpers
- Never store plaintext passwords
- OAuth tokens must be validated before use
- Implement rate limiting for auth endpoints
- Use secure session cookies (HttpOnly, Secure flags)

## Session Management

- Use Flask-Login for session handling
- Configure session timeouts (15-30 minutes for sensitive apps)
- Implement CSRF protection for all forms
- Regenerate session IDs after login

## Input Validation

- Validate all user inputs server-side
- Sanitize output to prevent XSS
- Use parameterized queries to prevent SQL injection
- Restrict file upload types and scan for malware

## HTTPS & Headers

- Enforce HTTPS in production
- Set security headers (CSP, XSS Protection, etc.)
- Implement CORS policies
- Disable directory listing
