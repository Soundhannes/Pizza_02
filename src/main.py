from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="Recipe API", version="1.0.0")

# In-memory storage for recipes
recipes_db = {}

class Recipe(BaseModel):
    id: Optional[str] = None
    name: str
    ingredients: List[str]
    instructions: str
    prep_time: int
    cook_time: int

@app.delete("/api/recipes/{recipe_id}")
async def delete_recipe(recipe_id: str):
    """
    Delete a recipe by ID
    """
    # Input validation - check if ID is provided and not empty
    if not recipe_id or not recipe_id.strip():
        raise HTTPException(status_code=400, detail="Recipe ID cannot be empty")
    
    # Check if recipe exists
    if recipe_id not in recipes_db:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Delete the recipe
    deleted_recipe = recipes_db.pop(recipe_id)
    
    return {"message": "Recipe deleted successfully", "deleted_recipe_id": recipe_id}

@app.get("/")
async def root():
    return {"message": "Recipe API is running"}