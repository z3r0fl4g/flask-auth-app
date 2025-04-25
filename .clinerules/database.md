# Database Rules

## Models

- All models must inherit from db.Model
- Relationships should be explicitly defined
- Password fields must be marked as non-serializable

## Migrations

- All schema changes require Alembic migrations
- Never modify production database directly
- Test migrations in development first

## Queries

- Use SQLAlchemy ORM for all database operations
- Avoid raw SQL queries when possible
- Use transactions for multiple related operations
