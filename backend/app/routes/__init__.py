"""Routes package for trading simulation backend."""
from .auth import auth_bp
from .portfolio import portfolio_bp
from .trading import trading_bp

__all__ = ['auth_bp', 'portfolio_bp', 'trading_bp']
