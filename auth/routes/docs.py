"""
Documentation routes for the application.

This module handles all documentation-related routes including:
- UI design system documentation
- API documentation
- Usage guides
"""

from flask import Blueprint, render_template

# Create documentation blueprint
docs_bp = Blueprint('docs', __name__)

@docs_bp.route('/ui-design')
def ui_design():
    """
    Display the UI design system documentation.
    
    Renders the uidesign.html template which showcases:
    - Color palette
    - Typography
    - Spacing system
    - UI components
    - Design principles
    
    Returns:
        Response: Rendered uidesign.html template
    """
    return render_template('uidesign.html')

@docs_bp.route('/')
def index():
    """
    Display the main documentation index.
    
    Provides links to all available documentation sections.
    
    Returns:
        Response: Rendered documentation index template
    """
    return render_template('uidesign.html')  # Temporarily redirects to UI design docs
