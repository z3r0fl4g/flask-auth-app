# Flask Authentication System

A secure authentication system built with Flask, SQLAlchemy, and Werkzeug security.

## Features

- User registration and login
- Secure password hashing
- Session management
- Password reset functionality
- Responsive UI with Tailwind CSS
- Database migrations with Alembic

## Project Structure

```
.
├── auth/                     # Authentication blueprint
│   ├── __init__.py           # Blueprint initialization
│   ├── models.py             # User models
│   ├── routes/               # Route handlers
│   │   ├── auth.py           # Authentication routes
│   │   └── oauth.py          # OAuth routes
│   └── templates/            # Authentication templates
├── migrations/               # Database migrations
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
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:

```bash
python init_db.py
```

## Usage

Run the development server:

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Configuration

Environment variables in `.env`:

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///auth.db
```

## Deployment

For production deployment:

1. Set `FLASK_ENV=production`
2. Configure a proper WSGI server (Gunicorn, uWSGI)
3. Set up a production database (PostgreSQL recommended)
4. Configure HTTPS

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
