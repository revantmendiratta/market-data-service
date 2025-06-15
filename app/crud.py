from sqlalchemy.orm import Session
from . import models, schemas
import datetime

def create_price_record(db: Session, price: schemas.PriceCreate):
    """
    Creates a new price record in the database.
    """
    # Create a database model instance from the Pydantic schema data
    db_price = models.Price(
        symbol=price.symbol,
        price=price.price,
        provider=price.provider,
        timestamp=datetime.datetime.fromisoformat(price.timestamp.replace("Z", "+00:00"))
    )
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price
def get_last_n_prices(db: Session, symbol: str, n: int):
    """
    Fetches the last N price records for a given symbol, ordered by timestamp.
    """
    return db.query(models.Price).filter(models.Price.symbol == symbol).order_by(models.Price.timestamp.desc()).limit(n).all()

def upsert_moving_average(db: Session, symbol: str, moving_average: float):
    """
    Updates the moving average for a symbol if it exists, otherwise creates it.
    """
    # Try to find an existing record for the symbol
    db_ma = db.query(models.MovingAverage).filter(models.MovingAverage.symbol == symbol).first()
    
    if db_ma:
        # If it exists, update it
        db_ma.moving_average = moving_average
    else:
        # If it doesn't exist, create a new one
        db_ma = models.MovingAverage(symbol=symbol, moving_average=moving_average)
        db.add(db_ma)
        
    db.commit()
    db.refresh(db_ma)
    return db_ma