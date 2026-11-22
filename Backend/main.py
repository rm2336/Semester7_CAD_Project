from fastapi import FastAPI, Depends, HTTPException
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

@app.get("/recipes/{recipeId}", response_model = schemas.Recipe)
def get_recipe(recipeId: int, db: Session=Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipeId).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found.")

@app.post("/recipes/", response_model=schemas.Recipe)
def post_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = models.Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@app.put("/recipes/{recipeId}")
def put_recipe(recipeId: int, recipe: schemas.RecipeCreate, db: Session=Depends(get_db)):
    db_item = db.query(models.Recipe).filter(models.Recipe.id == recipeId).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Recipe not found.")
    for field, value in recipe.dict().items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/recipes/{recipeId}")
def delete_recipe(recipeId: int, db: Session=Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipeId).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found.")
    db.delete(recipe)
    db.commit()
    return {"message": "Recipe successfully deleted."}

message = get_root()
print(message["message"])

