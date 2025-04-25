"""
OAuth authentication routes for third-party login providers.

Handles authentication with:
- Google
- GitHub 
- Instagram
- Twitter

Implements OAuth 2.0 flows using Authlib library.
Creates/updates user records in database upon successful auth.
"""

from flask import Blueprint, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from flask_login import login_user
from ..models import User  # We'll need to create this later

oauth_bp = Blueprint('oauth', __name__)
oauth = OAuth()

# OAuth configuration will go here
providers = ['google', 'github', 'instagram', 'twitter']

def init_oauth(app):
    """
    Initialize OAuth providers with app configuration.
    
    Args:
        app: Flask application instance
        
    Registers OAuth clients for all supported providers with:
    - Client IDs and secrets from config
    - Proper authorization endpoints
    - Required scopes for each provider
    - API base URLs
    
    Called during app initialization to set up OAuth integration.
    """
    # Google configuration
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        client_kwargs={'scope': 'openid email profile'}
    )

    # GitHub configuration
    oauth.register(
        name='github',
        client_id=app.config['GITHUB_CLIENT_ID'],
        client_secret=app.config['GITHUB_CLIENT_SECRET'],
        access_token_url='https://github.com/login/oauth/access_token',
        access_token_params=None,
        authorize_url='https://github.com/login/oauth/authorize',
        authorize_params=None,
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'}
    )

    # Instagram configuration
    oauth.register(
        name='instagram',
        client_id=app.config['INSTAGRAM_CLIENT_ID'],
        client_secret=app.config['INSTAGRAM_CLIENT_SECRET'],
        access_token_url='https://api.instagram.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://api.instagram.com/oauth/authorize',
        authorize_params=None,
        api_base_url='https://graph.instagram.com/',
        client_kwargs={'scope': 'user_profile,user_media'}
    )

    # Twitter (X) configuration
    oauth.register(
        name='twitter',
        client_id=app.config['TWITTER_CLIENT_ID'],
        client_secret=app.config['TWITTER_CLIENT_SECRET'],
        access_token_url='https://api.twitter.com/2/oauth2/token',
        access_token_params=None,
        authorize_url='https://twitter.com/i/oauth2/authorize',
        authorize_params=None,
        api_base_url='https://api.twitter.com/2/',
        client_kwargs={'scope': 'users.read tweet.read'}
    )

@oauth_bp.route('/login/<provider>')
def login(provider):
    """
    Initiate OAuth flow for specified provider.
    
    Args:
        provider: Name of OAuth provider (google/github/instagram/twitter)
        
    Returns:
        Response: Redirect to provider's authorization endpoint
        
    Raises:
        400 Error if provider is not supported
    """
    if provider not in providers:
        return "Invalid provider", 400
        
    redirect_uri = url_for('oauth.authorize', provider=provider, _external=True)
    return oauth.create_client(provider).authorize_redirect(redirect_uri)

@oauth_bp.route('/authorize/<provider>')
def authorize(provider):
    """
    Handle OAuth callback from provider.
    
    Args:
        provider: Name of OAuth provider
        
    Returns:
        Response: Redirect to home page after successful authentication
        
    Raises:
        400 Error if provider is not supported
        
    Handles:
        - Access token exchange
        - User info retrieval
        - User creation/updating
        - Session creation
    """
    if provider not in providers:
        return "Invalid provider", 400
        
    client = oauth.create_client(provider)
    token = client.authorize_access_token()
    
    # Handle different provider responses
    if provider == 'github':
        user_info = client.get('user').json()
        user_info['sub'] = str(user_info['id'])  # Map to standard 'sub' claim
    elif provider == 'instagram':
        user_info = client.get('me', params={'fields': 'id,username'}).json()
        user_info['sub'] = user_info['id']
        user_info['name'] = user_info['username']
    elif provider == 'twitter':
        user_info = client.get('users/me', params={'user.fields': 'id,name,profile_image_url'}).json()['data']
        user_info['sub'] = user_info['id']
        user_info['picture'] = user_info.get('profile_image_url')
    else:  # Google and standard OIDC providers
        user_info = client.parse_id_token(token)
    
    # Create/get user and log them in
    user = User.get_or_create(provider, user_info)
    login_user(user)
    
    return redirect(url_for('index'))
