"""Portfolio management routes for the trading simulation backend."""
from flask import Blueprint

portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')

@portfolio_bp.route('/status', methods=['GET'])
def get_portfolio_status():
    """Get current portfolio status."""
    return {'message': 'Portfolio route is working'}
