from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.routes import analyze

app = FastAPI(title="DermSight API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(analyze.router)

@app.get("/")
def root():
    return {"message": "DermSight Backend Running"}
