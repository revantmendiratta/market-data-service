from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..services.market_data_provider import get_provider
from ..core.database import get_db
from .. import schemas, crud
from ..services.kafka_producer import produce_price_event
import datetime

router = APIRouter()

# --- KEEP ONLY THIS VERSION ---
@router.get("/latest", response_model=schemas.PriceResponse)
def get_latest_price(symbol: str, provider: str, db: Session = Depends(get_db)):
    market_data_provider = get_provider(provider)
    price_data = market_data_provider.get_latest_price(symbol)

    if "error" in price_data:
        raise HTTPException(status_code=404, detail=price_data["error"])

    # Create the full data object, including a timestamp
    full_price_data = schemas.PriceCreate(
        symbol=price_data["symbol"],
        price=price_data["price"],
        provider=price_data["provider"],
        timestamp=datetime.datetime.utcnow().isoformat() + "Z"
    )

    # Use the CRUD function to save the data to the database
    crud.create_price_record(db=db, price=full_price_data)

    # PRODUCE MESSAGE TO KAFKA
    # We produce the raw dictionary, not the Pydantic model
    produce_price_event(full_price_data.dict())

    # Return the data as the response
    return full_price_data