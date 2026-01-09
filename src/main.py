from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import Dict, Any, Optional
import re

app = FastAPI(title="Widget API", version="1.0.0")

# In-memory storage for widgets (in production, use a database)
widgets_storage: Dict[str, Dict[str, Any]] = {}

class WidgetConfig(BaseModel):
    key: str
    config: Dict[str, Any]

def validate_widget_key(key: str) -> str:
    """Validate widget key format"""
    if not key:
        raise HTTPException(status_code=400, detail="Widget key cannot be empty")
    
    if len(key) > 100:
        raise HTTPException(status_code=400, detail="Widget key too long (max 100 characters)")
    
    # Allow alphanumeric, hyphens, underscores
    if not re.match(r'^[a-zA-Z0-9_-]+$', key):
        raise HTTPException(
            status_code=400, 
            detail="Widget key can only contain alphanumeric characters, hyphens, and underscores"
        )
    
    return key

@app.get("/api/widgets/{key}")
async def get_widget(
    key: str = Path(..., description="Widget key", min_length=1, max_length=100)
) -> Dict[str, Any]:
    """
    Get widget configuration by key
    
    Args:
        key: The widget key to retrieve
        
    Returns:
        Widget configuration
        
    Raises:
        HTTPException: 400 for invalid key format, 404 if widget not found
    """
    try:
        # Validate key format
        validated_key = validate_widget_key(key)
        
        # Check if widget exists
        if validated_key not in widgets_storage:
            raise HTTPException(
                status_code=404, 
                detail=f"Widget with key '{validated_key}' not found"
            )
        
        return widgets_storage[validated_key]
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500, 
            detail="Internal server error occurred while retrieving widget"
        )

@app.post("/api/widgets")
async def create_widget(widget: WidgetConfig) -> Dict[str, str]:
    """Create a new widget (helper endpoint for testing)"""
    validated_key = validate_widget_key(widget.key)
    widgets_storage[validated_key] = widget.config
    return {"message": f"Widget '{validated_key}' created successfully"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)