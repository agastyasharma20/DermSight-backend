from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, analyze

app = FastAPI(
    title="DermSight API",
    description="AI-powered dermatology triage system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hackathon only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(analyze.router)

@app.get("/")
def root():
    return {"message": "DermSight Backend Running"}
from app.db.database import engine, Base
from app.models import models
from app.models.case import Case

Base.metadata.create_all(bind=engine)
