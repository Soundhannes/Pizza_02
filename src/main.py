from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI(title="Recipe API", version="1.0.0")

# Pydantic models
class Recipe(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    ingredients: list[str]
    instructions: list[str]
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    servings: Optional[int] = None

# Mock data for demonstration
RECIPES_DB = {
    "550e8400-e29b-41d4-a716-446655440000": Recipe(
        id="550e8400-e29b-41d4-a716-446655440000",
        name="Spaghetti Carbonara",
        description="Classic Italian pasta dish",
        ingredients=["spaghetti", "eggs", "bacon", "parmesan cheese", "black pepper"],
        instructions=[
            "Cook spaghetti according to package instructions",
            "Fry bacon until crispy",
            "Mix eggs with parmesan cheese",
            "Combine hot pasta with egg mixture",
            "Add bacon and season with pepper"
        ],
        prep_time=10,
        cook_time=15,
        servings=4
    ),
    "6ba7b810-9dad-11d1-80b4-00c04fd430c8": Recipe(
        id="6ba7b810-9dad-11d1-80b4-00c04fd430c8",
        name="Chocolate Chip Cookies",
        description="Homemade chocolate chip cookies",
        ingredients=["flour", "butter", "sugar", "eggs", "chocolate chips"],
        instructions=[
            "Preheat oven to 375°F",
            "Mix dry ingredients",
            "Cream butter and sugar",
            "Add eggs and mix",
            "Combine wet and dry ingredients",
            "Add chocolate chips",
            "Bake for 10-12 minutes"
        ],
        prep_time=20,
        cook_time=12,
        servings=24
    )
}

def is_valid_uuid(value: str) -> bool:
    """Validate if string is a valid UUID format"""
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False

@app.get("/api/recipes/{id}", response_model=Recipe)
async def get_recipe(id: str):
    """
    Get a specific recipe by ID
    
    Args:
        id: Recipe ID (must be valid UUID format)
        
    Returns:
        Recipe object
        
    Raises:
        HTTPException: 400 for invalid ID format, 404 for recipe not found
    """
    # Input validation
    if not id:
        raise HTTPException(status_code=400, detail="Recipe ID cannot be empty")
    
    if not is_valid_uuid(id):
        raise HTTPException(status_code=400, detail="Invalid recipe ID format. Must be a valid UUID")
    
    # Check if recipe exists
    if id not in RECIPES_DB:
        raise HTTPException(status_code=404, detail=f"Recipe with ID {id} not found")
    
    return RECIPES_DB[id]

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Recipe API is running"}