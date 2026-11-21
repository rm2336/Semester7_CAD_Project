from fastapi import FastAPI
from sqlalchemy.orm import Session

from database import SessionLocal, engine

import models, schemas

models.Base.metadata.create_all(bind=engine)

# Instantiate the FastAPI application
app = FastAPI()

# Fetch the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define API endpoints
@app.get("/")
def get_root():
    return {"message": "Welcome to my recipe app!"}

