from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Stock(Base):
    """Stock model for tracking available stocks and their information."""
    __tablename__ = 'stocks'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), unique=True, nullable=False)  # Stock ticker symbol (e.g., 'AAPL')
    name = Column(String(255), nullable=False)  # Company name
    current_price = Column(Float, nullable=False, default=0.0)
    previous_close = Column(Float, nullable=False, default=0.0)
    market_cap = Column(Float, default=0.0)
    sector = Column(String(100))
    industry = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Stock {self.symbol}: {self.name}>'
    
    def to_dict(self):
        """Convert Stock object to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'current_price': self.current_price,
            'previous_close': self.previous_close,
            'market_cap': self.market_cap,
            'sector': self.sector,
            'industry': self.industry,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @property
    def price_change(self):
        """Calculate price change from previous close."""
        return self.current_price - self.previous_close
    
    @property
    def price_change_percent(self):
        """Calculate percentage price change from previous close."""
        if self.previous_close == 0:
            return 0.0
        return (self.price_change / self.previous_close) * 100
