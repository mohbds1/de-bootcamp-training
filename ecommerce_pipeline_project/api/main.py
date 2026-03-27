from fastapi import FastAPI

from api.database.database import Base, engine
from api.routers.orders import router as orders_router

app = FastAPI(
    title="E-commerce Orders Monitoring API",
    version="1.0.0",
    description="API for accessing latest clean e-commerce orders and their statistics.",
)

Base.metadata.create_all(bind=engine)
app.include_router(orders_router)


@app.get("/")
def root():
    return {
        "message": "E-commerce Orders Monitoring API is running.",
        "docs": "/docs",
    }
