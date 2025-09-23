from flask import Blueprint, request, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from app.models.user import User, db
from app.services.rating_service import RatingService
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user - POST /api/auth/register"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'phone', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'error': f'{field.capitalize()} is required'
                }), 400
        
        name = data['name'].strip()
        phone = data['phone'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        
        # Validate input lengths
        if len(name) < 2:
            return jsonify({'error': 'Name must be at least 2 characters long'}), 400
        if len(phone) < 10:
            return jsonify({'error': 'Phone number must be at least 10 digits'}), 400
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter(
            (User.email == email) | (User.phone == phone)
        ).first()
        
        if existing_user:
            if existing_user.email == email:
                return jsonify({'error': 'Email already registered'}), 400
            else:
                return jsonify({'error': 'Phone number already registered'}), 400
        
        # Create new user
        user = User(name=name, phone=phone, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
        # Log the user in
        login_user(user)
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Registration failed',
            'details': str(e)
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user login"""
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                return jsonify({'error': 'Account is deactivated'}), 403
            
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'message': 'Login successful',
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
            
    except Exception as e:
        return jsonify({
            'error': 'Login failed',
            'details': str(e)
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout current user"""
    try:
        logout_user()
        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        return jsonify({
            'error': 'Logout failed',
            'details': str(e)
        }), 500

@auth_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """Get current user profile"""
    try:
        return jsonify({
            'user': current_user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'error': 'Failed to get profile',
            'details': str(e)
        }), 500

@auth_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    """Update current user profile"""
    try:
        data = request.get_json()
        
        # Update allowed fields
        if 'name' in data:
            name = data['name'].strip()
            if len(name) >= 2:
                current_user.name = name
            else:
                return jsonify({'error': 'Name must be at least 2 characters long'}), 400
        
        current_user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': current_user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Profile update failed',
            'details': str(e)
        }), 500
