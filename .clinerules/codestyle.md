# Code Style Guidelines

## Python Formatting

- Follow PEP 8 with 4-space indentation
- Use Google-style docstrings for all functions/classes
- Keep line length under 100 characters

## Flask Specifics

- Route handlers should be in separate blueprint modules
- Use `url_for()` for all internal URL generation
- Keep business logic out of route handlers

## Template Formatting

- Use 2-space indentation in HTML templates
- Keep template logic minimal
- Use template inheritance with base.html
