from fastapi import FastAPI
from .core.database import engine, Base
from .api import prices # Import the new router

# Create all database tables defined in our models
# This is simple for a demo, for production you'd use migration tools like Alembic
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blockhouse Market Data Service",
    description="A service to fetch, process, and serve market data.",
    version="1.0.0"
)

# Include the prices router in our main app
app.include_router(prices.router, prefix="/prices", tags=["prices"])


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the Market Data Service!"}