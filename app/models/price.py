from sqlalchemy import Column, Integer, String, Float, DateTime
from ..core.database import Base
import datetime

class Price(Base):
    __tablename__ = "processed_price_points"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    provider = Column(String, nullable=False)

class MovingAverage(Base):
    __tablename__ = "symbol_averages"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    moving_average = Column(Float, nullable=False)