from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()

class TradeType(Enum):
    """Enumeration for trade types."""
    BUY = "BUY"
    SELL = "SELL"

class TradeStatus(Enum):
    """Enumeration for trade status."""
    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    CANCELLED = "CANCELLED"
    PARTIAL = "PARTIAL"

class Trade(db.Model):
    """Trade model for storing trading transactions and history."""
    __tablename__ = 'trades'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # User relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Trade details
    symbol = db.Column(db.String(10), nullable=False)  # Stock symbol (e.g., 'AAPL', 'TSLA')
    company_name = db.Column(db.String(200))  # Full company name
    trade_type = db.Column(db.Enum(TradeType), nullable=False)  # BUY or SELL
    quantity = db.Column(db.Integer, nullable=False)  # Number of shares
    
    # Price information
    price_per_share = db.Column(db.Float, nullable=False)  # Price at which trade was executed
    total_amount = db.Column(db.Float, nullable=False)  # quantity * price_per_share
    
    # Market data at time of trade
    market_price = db.Column(db.Float)  # Current market price when trade was placed
    
    # Trade execution
    status = db.Column(db.Enum(TradeStatus), default=TradeStatus.PENDING)
    executed_at = db.Column(db.DateTime)  # When the trade was executed
    
    # Profit/Loss tracking
    current_price = db.Column(db.Float)  # Current market price (updated periodically)
    unrealized_pnl = db.Column(db.Float, default=0.0)  # Unrealized profit/loss
    realized_pnl = db.Column(db.Float, default=0.0)  # Realized profit/loss (when sold)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # When trade was placed
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional metadata
    notes = db.Column(db.Text)  # User notes about the trade
    is_active = db.Column(db.Boolean, default=True)  # Whether position is still active
    
    def __init__(self, user_id, symbol, trade_type, quantity, price_per_share, 
                 company_name=None, market_price=None, notes=None):
        self.user_id = user_id
        self.symbol = symbol.upper()
        self.company_name = company_name
        self.trade_type = trade_type
        self.quantity = quantity
        self.price_per_share = price_per_share
        self.total_amount = quantity * price_per_share
        self.market_price = market_price or price_per_share
        self.current_price = price_per_share
        self.notes = notes
    
    def execute_trade(self):
        """Mark trade as executed."""
        self.status = TradeStatus.EXECUTED
        self.executed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def cancel_trade(self):
        """Cancel a pending trade."""
        if self.status == TradeStatus.PENDING:
            self.status = TradeStatus.CANCELLED
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def update_current_price(self, new_price):
        """Update current market price and calculate unrealized P&L."""
        self.current_price = new_price
        
        if self.status == TradeStatus.EXECUTED and self.is_active:
            if self.trade_type == TradeType.BUY:
                # For buy trades, profit when current price > buy price
                self.unrealized_pnl = (new_price - self.price_per_share) * self.quantity
            else:  # SELL trades
                # For sell trades, profit when current price < sell price
                self.unrealized_pnl = (self.price_per_share - new_price) * self.quantity
        
        self.updated_at = datetime.utcnow()
    
    def close_position(self, closing_price=None):
        """Close the position and realize P&L."""
        if not self.is_active:
            return False
        
        closing_price = closing_price or self.current_price
        
        if self.trade_type == TradeType.BUY:
            self.realized_pnl = (closing_price - self.price_per_share) * self.quantity
        else:  # SELL trades
            self.realized_pnl = (self.price_per_share - closing_price) * self.quantity
        
        self.unrealized_pnl = 0.0
        self.is_active = False
        self.updated_at = datetime.utcnow()
        
        return True
    
    def get_profit_percentage(self):
        """Calculate profit percentage based on initial investment."""
        if self.total_amount == 0:
            return 0.0
        
        if self.is_active:
            profit = self.unrealized_pnl
        else:
            profit = self.realized_pnl
        
        return (profit / self.total_amount) * 100
    
    def get_trade_value(self):
        """Get current value of the trade."""
        if self.trade_type == TradeType.BUY and self.is_active:
            return self.quantity * self.current_price
        return self.total_amount
    
    def to_dict(self):
        """Convert trade object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'symbol': self.symbol,
            'company_name': self.company_name,
            'trade_type': self.trade_type.value if self.trade_type else None,
            'quantity': self.quantity,
            'price_per_share': self.price_per_share,
            'total_amount': self.total_amount,
            'market_price': self.market_price,
            'current_price': self.current_price,
            'status': self.status.value if self.status else None,
            'unrealized_pnl': self.unrealized_pnl,
            'realized_pnl': self.realized_pnl,
            'profit_percentage': self.get_profit_percentage(),
            'trade_value': self.get_trade_value(),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'executed_at': self.executed_at.isoformat() if self.executed_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'notes': self.notes
        }
    
    def __repr__(self):
        return f'<Trade {self.trade_type.value if self.trade_type else ""} {self.quantity} {self.symbol} @ ${self.price_per_share}>'
