from fastapi import FastAPI
from app.db.database import engine, Base
from app.routes import analyze  # adjust if your router path differs

app = FastAPI(
    title="DermSight API",
    version="1.0.0"
)

# Create tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(analyze.router)

@app.get("/")
def root():
    return {"message": "DermSight Backend Running"}
