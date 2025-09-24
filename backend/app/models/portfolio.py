from .. import db
from datetime import datetime

class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    avg_price = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with User model
    user = db.relationship('User', backref='portfolio_holdings')
    
    def __repr__(self):
        return f'<Portfolio {self.user_id}:{self.symbol} qty:{self.quantity}>'
    
    @property
    def total_value(self):
        """Calculate total value of this position"""
        return self.quantity * self.avg_price
    
    def update_position(self, new_quantity, new_price):
        """Update portfolio position with new trade data"""
        if self.quantity == 0:
            self.avg_price = new_price
        else:
            total_cost = (self.quantity * self.avg_price) + (new_quantity * new_price)
            total_quantity = self.quantity + new_quantity
            if total_quantity > 0:
                self.avg_price = total_cost / total_quantity
            else:
                self.avg_price = 0.0
        
        self.quantity += new_quantity
        self.updated_at = datetime.utcnow()
