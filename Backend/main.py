from fastapi import FastAPI, Depends
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

@app.get("/recipes/", response_model=list[schemas.Recipe])
def get_recipes(skip: int=0, limit: int=50, db: Session=Depends(get_db)):
    recipes = db.query(models.Recipe).offset(skip).limit(limit).all()
    return recipes

@app.post("/recipes/", response_model=schemas.Recipe)
def post_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = models.Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

