from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

app = FastAPI(title="Recipe API", version="1.0.0")

# In-memory storage for recipes
recipes_db = {}

class Recipe(BaseModel):
    id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    ingredients: List[str] = Field(..., min_items=1)
    instructions: List[str] = Field(..., min_items=1)
    prep_time: Optional[int] = Field(None, ge=0)
    cook_time: Optional[int] = Field(None, ge=0)
    servings: Optional[int] = Field(None, ge=1)

class RecipeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    ingredients: Optional[List[str]] = Field(None, min_items=1)
    instructions: Optional[List[str]] = Field(None, min_items=1)
    prep_time: Optional[int] = Field(None, ge=0)
    cook_time: Optional[int] = Field(None, ge=0)
    servings: Optional[int] = Field(None, ge=1)

@app.put("/api/recipes/{id}")
async def update_recipe(id: str, recipe_update: RecipeUpdate):
    # Check if recipe exists
    if id not in recipes_db:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Get existing recipe
    existing_recipe = recipes_db[id]
    
    # Update only provided fields
    update_data = recipe_update.dict(exclude_unset=True)
    
    # Validate that lists are not empty if provided
    if "ingredients" in update_data and len(update_data["ingredients"]) == 0:
        raise HTTPException(status_code=422, detail="Ingredients list cannot be empty")
    
    if "instructions" in update_data and len(update_data["instructions"]) == 0:
        raise HTTPException(status_code=422, detail="Instructions list cannot be empty")
    
    # Update the recipe
    for field, value in update_data.items():
        setattr(existing_recipe, field, value)
    
    # Store updated recipe
    recipes_db[id] = existing_recipe
    
    return existing_recipe

@app.post("/api/recipes")
async def create_recipe(recipe: Recipe):
    recipe_id = str(uuid.uuid4())
    recipe.id = recipe_id
    recipes_db[recipe_id] = recipe
    return recipe

@app.get("/api/recipes/{id}")
async def get_recipe(id: str):
    if id not in recipes_db:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipes_db[id]

@app.get("/api/recipes")
async def get_recipes():
    return list(recipes_db.values())

@app.delete("/api/recipes/{id}")
async def delete_recipe(id: str):
    if id not in recipes_db:
        raise HTTPException(status_code=404, detail="Recipe not found")
    del recipes_db[id]
    return {"message": "Recipe deleted successfully"}