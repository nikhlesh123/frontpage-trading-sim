#!/usr/bin/env python3
"""
Frontpage Trading Sim - Flask Application Entry Point

This is the main entry point for the Flask application.
It creates the Flask app instance and runs the development server.
"""

import os
from app import create_app
from config import config

def main():
    """Main function to run the Flask application."""
    # Get configuration environment
    config_name = os.getenv('FLASK_CONFIG', 'default')
    
    # Create Flask app with configuration
    app = create_app(config[config_name])
    
    # Get host and port from environment or use defaults
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() in ['true', '1', 'on']
    
    print(f"Starting Frontpage Trading Sim server...")
    print(f"Environment: {config_name}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print("\n" + "="*50)
    print("IMPORTANT: AngelOne API Configuration Required")
    print("="*50)
    print("Before using the application, please:")
    print("1. Obtain API credentials from AngelOne")
    print("2. Update the configuration in config.py")
    print("3. Or set environment variables:")
    print("   - ANGELONE_API_KEY")
    print("   - ANGELONE_CLIENT_CODE")
    print("   - ANGELONE_PASSWORD")
    print("   - ANGELONE_TOTP_SECRET")
    print("="*50 + "\n")
    
    # Run the Flask application
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug,
        threaded=True
    )

if __name__ == '__main__':
    main()
