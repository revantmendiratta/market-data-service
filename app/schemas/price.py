from pydantic import BaseModel, ConfigDict
import datetime

class PriceCreate(BaseModel):
    symbol: str
    price: float
    timestamp: str
    provider: str

# Modify the PriceResponse class like this
class PriceResponse(BaseModel):
    symbol: str
    price: float
    timestamp: str
    provider: str

    # Replace the inner Config class with this model_config variable
    model_config = ConfigDict(from_attributes=True)