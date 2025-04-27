# Flask Authentication System

A comprehensive authentication system built with Flask, featuring modern UI design and robust security features.

## Features

- **Authentication Methods**

  - Local email/password authentication
  - OAuth integration (Google, GitHub, Twitter, Instagram)
  - Two-factor authentication (Email verification)

- **Security Features**

  - Secure password hashing with Werkzeug
  - Time-limited password reset tokens
  - Rate limiting for sensitive endpoints
  - CSRF protection
  - Secure session management

- **User Experience**

  - Modern, responsive UI with Tailwind CSS
  - Consistent design system
  - Intuitive authentication flows
  - Glassmorphism and subtle animations

- **Developer Features**
  - Database migrations with Alembic/Flask-Migrate
  - Comprehensive documentation
  - Modular blueprint architecture

## Project Structure

```
.
├── auth/                     # Authentication package
│   ├── __init__.py           # Package initialization
│   ├── models.py             # User and auth models
│   ├── routes/               # Route handlers
│   │   ├── __init__.py       # Routes package
│   │   ├── auth.py           # Core authentication routes
│   │   ├── oauth.py          # OAuth provider routes
│   │   ├── twofa.py          # Two-factor auth routes
│   │   └── docs.py           # Documentation routes
│   └── templates/            # Jinja2 templates
│       ├── base.html         # Base template with layout
│       ├── index.html        # Landing page
│       ├── login.html        # Login form
│       ├── signup.html       # Registration form
│       ├── twofa_*.html      # 2FA templates
│       └── ...               # Other templates
├── migrations/               # Database migrations
├── static/                   # Static assets
├── app.py                    # Main application
├── init_db.py                # Database initialization
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/flask-auth.git
cd flask-auth
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
# Create a .env file with the following variables
FLASK_SECRET_KEY=your-secure-secret-key

# OAuth credentials (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

5. Initialize the database:

```bash
python init_db.py
```

6. Run database migrations:

```bash
python run_migrations.py
```

This will apply all pending migrations to update the database schema.

## Usage

Run the development server:

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Key URLs

- `/` - Home page
- `/auth/login` - Login page
- `/auth/signup` - Registration page
- `/auth/2fa/settings` - Two-factor authentication settings
- `/docs/ui-design` - UI design system documentation

## Security Features

### Password Security

- Passwords are hashed using Werkzeug's security functions
- Password reset uses time-limited tokens
- OAuth integration avoids password storage for social logins

### Two-Factor Authentication

- Email-based verification codes
- Time-limited codes (15 minutes)
- Rate-limited code resending (3 per hour)
- Secure code storage with bcrypt

### Session Security

- Secure cookie settings (HttpOnly, SameSite)
- Session regeneration after critical actions
- CSRF protection on all forms

## UI Design System

The application follows a consistent design system with:

- **Color Palette**: Primary rose color with complementary accents
- **Typography**: Inter font family with consistent sizing
- **Components**: Standardized buttons, forms, and cards
- **Spacing**: 8px grid system for consistent layout
- **Principles**: Clarity, responsiveness, and accessibility

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
