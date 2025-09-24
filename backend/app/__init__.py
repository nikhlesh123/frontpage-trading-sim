"""
Flask Application Factory
This module contains the Flask application factory function.
It initializes and configures the Flask application with all necessary extensions.
"""
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_class):
    """Create and configure the Flask application.
    
    Args:
        config_class: Configuration class containing app settings
        
    Returns:
        Flask: Configured Flask application instance
    """
    # Path to React build directory
    frontend_build_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', '..', 'frontend', 'build'
    ))
    
    # Create Flask app instance with proper static folder configuration
    app = Flask(__name__, 
                instance_relative_config=True,
                static_folder=frontend_build_path,
                static_url_path='')
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    
    # Configure CORS - allow production domains for deployed app
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:3000", 
                "http://127.0.0.1:3000",
                "https://*.onrender.com",  # Allow Render deployment domains
                "https://*.herokuapp.com",  # Allow Heroku deployment domains
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.trading import trading_bp
    from app.routes.portfolio import portfolio_bp
    from app.routes.user import user_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(trading_bp, url_prefix='/api/trading')
    app.register_blueprint(portfolio_bp, url_prefix='/api/portfolio')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    
    # Register error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'Bad request'}, 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return {'error': 'Unauthorized'}, 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return {'error': 'Forbidden'}, 403
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Frontpage Trading Sim API is running'}
    
    # Serve React frontend for all non-API routes
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react_app(path):
        """Serve the React frontend for all non-API routes."""
        # If the path starts with 'api', it should be handled by API routes
        if path.startswith('api/'):
            return {'error': 'API endpoint not found'}, 404
        
        # Try to serve static files first (JS, CSS, images, etc.)
        if path and '.' in path.split('/')[-1]:
            try:
                return send_from_directory(frontend_build_path, path)
            except:
                # If file not found, fall through to serve index.html
                pass
        
        # For all other paths, serve the React app's index.html
        return send_from_directory(frontend_build_path, 'index.html')
    
    return app
