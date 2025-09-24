from flask import Blueprint

# Create trading blueprint
trading_bp = Blueprint('trading', __name__)

@trading_bp.route('/api/trading', methods=['GET'])
def get_trading_data():
    """Get trading data endpoint"""
    return {'message': 'Trading data endpoint'}

@trading_bp.route('/api/trading/portfolio', methods=['GET'])
def get_portfolio():
    """Get portfolio data endpoint"""
    return {'message': 'Portfolio data endpoint'}
