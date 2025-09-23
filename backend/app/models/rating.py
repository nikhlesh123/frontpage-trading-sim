from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Rating(db.Model):
    """Rating model for tracking user rating changes over time (Codeforces-style)."""
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # User relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Rating information
    old_rating = db.Column(db.Integer, nullable=False)  # Rating before the change
    new_rating = db.Column(db.Integer, nullable=False)  # Rating after the change
    rating_change = db.Column(db.Integer, nullable=False)  # Change in rating (+/-)
    
    # Performance metrics that led to rating change
    profit_percentage = db.Column(db.Float, nullable=False)  # Profit % for this period/contest
    trades_count = db.Column(db.Integer, default=0)  # Number of trades in this period
    win_rate = db.Column(db.Float, default=0.0)  # Percentage of profitable trades
    
    # Contest/period information
    contest_name = db.Column(db.String(200))  # Name/description of the contest/period
    contest_duration = db.Column(db.Integer)  # Duration in minutes/hours
    rank = db.Column(db.Integer)  # User's rank in this contest (if applicable)
    total_participants = db.Column(db.Integer)  # Total participants in contest
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Additional metadata
    notes = db.Column(db.Text)  # Additional notes about this rating change
    is_provisional = db.Column(db.Boolean, default=False)  # Whether this rating is provisional
    
    def __init__(self, user_id, old_rating, new_rating, profit_percentage, 
                 trades_count=0, win_rate=0.0, contest_name=None, 
                 contest_duration=None, rank=None, total_participants=None, notes=None):
        self.user_id = user_id
        self.old_rating = old_rating
        self.new_rating = new_rating
        self.rating_change = new_rating - old_rating
        self.profit_percentage = profit_percentage
        self.trades_count = trades_count
        self.win_rate = win_rate
        self.contest_name = contest_name
        self.contest_duration = contest_duration
        self.rank = rank
        self.total_participants = total_participants
        self.notes = notes
    
    def get_rating_title(self, rating=None):
        """Get Codeforces-style rating title based on rating value."""
        rating = rating or self.new_rating
        
        if rating < 1200:
            return "Newbie"
        elif rating < 1400:
            return "Pupil"
        elif rating < 1600:
            return "Specialist"
        elif rating < 1900:
            return "Expert"
        elif rating < 2100:
            return "Candidate Master"
        elif rating < 2300:
            return "Master"
        elif rating < 2400:
            return "International Master"
        elif rating < 2600:
            return "Grandmaster"
        elif rating < 3000:
            return "International Grandmaster"
        else:
            return "Legendary Grandmaster"
    
    def get_rating_color(self, rating=None):
        """Get Codeforces-style color code for rating."""
        rating = rating or self.new_rating
        
        if rating < 1200:
            return "#808080"  # Gray
        elif rating < 1400:
            return "#008000"  # Green
        elif rating < 1600:
            return "#03A89E"  # Cyan
        elif rating < 1900:
            return "#0000FF"  # Blue
        elif rating < 2100:
            return "#AA00AA"  # Purple
        elif rating < 2300:
            return "#FF8C00"  # Orange
        elif rating < 2400:
            return "#FF8C00"  # Orange
        elif rating < 2600:
            return "#FF0000"  # Red
        elif rating < 3000:
            return "#FF0000"  # Red
        else:
            return "#AA0000"  # Dark Red
    
    def is_rating_increase(self):
        """Check if this was a rating increase."""
        return self.rating_change > 0
    
    def get_performance_grade(self):
        """Get a performance grade based on profit percentage."""
        if self.profit_percentage >= 20:
            return "A+"
        elif self.profit_percentage >= 15:
            return "A"
        elif self.profit_percentage >= 10:
            return "A-"
        elif self.profit_percentage >= 5:
            return "B+"
        elif self.profit_percentage >= 0:
            return "B"
        elif self.profit_percentage >= -5:
            return "B-"
        elif self.profit_percentage >= -10:
            return "C+"
        elif self.profit_percentage >= -15:
            return "C"
        elif self.profit_percentage >= -20:
            return "C-"
        else:
            return "F"
    
    def to_dict(self):
        """Convert rating object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'old_rating': self.old_rating,
            'new_rating': self.new_rating,
            'rating_change': self.rating_change,
            'old_rating_title': self.get_rating_title(self.old_rating),
            'new_rating_title': self.get_rating_title(self.new_rating),
            'old_rating_color': self.get_rating_color(self.old_rating),
            'new_rating_color': self.get_rating_color(self.new_rating),
            'profit_percentage': self.profit_percentage,
            'performance_grade': self.get_performance_grade(),
            'trades_count': self.trades_count,
            'win_rate': self.win_rate,
            'contest_name': self.contest_name,
            'contest_duration': self.contest_duration,
            'rank': self.rank,
            'total_participants': self.total_participants,
            'is_rating_increase': self.is_rating_increase(),
            'is_provisional': self.is_provisional,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'notes': self.notes
        }
    
    def __repr__(self):
        sign = '+' if self.rating_change >= 0 else ''
        return f'<Rating {self.old_rating} → {self.new_rating} ({sign}{self.rating_change})>'
