from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for trader registration and authentication."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Trading related fields
    initial_balance = db.Column(db.Float, default=100000.0)  # Starting virtual balance
    current_balance = db.Column(db.Float, default=100000.0)
    total_profit_loss = db.Column(db.Float, default=0.0)
    
    # Rating system fields (Codeforces-style)
    rating = db.Column(db.Integer, default=1200)  # Starting rating like Codeforces
    max_rating = db.Column(db.Integer, default=1200)
    contests_participated = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Relationships
    trades = db.relationship('Trade', backref='trader', lazy=True, cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, name, phone, email, password):
        self.name = name
        self.phone = phone
        self.email = email
        self.set_password(password)
    
    def set_password(self, password):
        """Create password hash from plaintext password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash."""
        return check_password_hash(self.password_hash, password)
    
    def update_balance(self, amount):
        """Update current balance and calculate profit/loss."""
        old_balance = self.current_balance
        self.current_balance += amount
        self.total_profit_loss = self.current_balance - self.initial_balance
        self.updated_at = datetime.utcnow()
    
    def get_profit_percentage(self):
        """Calculate profit percentage from initial balance."""
        if self.initial_balance == 0:
            return 0.0
        return ((self.current_balance - self.initial_balance) / self.initial_balance) * 100
    
    def get_rating_title(self):
        """Get Codeforces-style rating title based on current rating."""
        if self.rating < 1200:
            return "Newbie"
        elif self.rating < 1400:
            return "Pupil"
        elif self.rating < 1600:
            return "Specialist"
        elif self.rating < 1900:
            return "Expert"
        elif self.rating < 2100:
            return "Candidate Master"
        elif self.rating < 2300:
            return "Master"
        elif self.rating < 2400:
            return "International Master"
        elif self.rating < 2600:
            return "Grandmaster"
        elif self.rating < 3000:
            return "International Grandmaster"
        else:
            return "Legendary Grandmaster"
    
    def to_dict(self):
        """Convert user object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'current_balance': self.current_balance,
            'total_profit_loss': self.total_profit_loss,
            'profit_percentage': self.get_profit_percentage(),
            'rating': self.rating,
            'max_rating': self.max_rating,
            'rating_title': self.get_rating_title(),
            'contests_participated': self.contests_participated,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active,
            'is_verified': self.is_verified
        }
    
    def __repr__(self):
        return f'<User {self.name} ({self.email})>'
