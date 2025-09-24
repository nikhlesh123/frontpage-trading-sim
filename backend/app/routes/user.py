"""User routes for trading simulation backend."""

from flask import Blueprint

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

@user_bp.route('/profile', methods=['GET'])
def get_profile():
    """Get user profile endpoint."""
    return {'message': 'User profile endpoint'}

@user_bp.route('/profile', methods=['PUT'])
def update_profile():
    """Update user profile endpoint."""
    return {'message': 'Profile updated successfully'}
