from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import re

app = FastAPI(title="Widget API", version="1.0.0")

# Pydantic models for validation
class WidgetResponse(BaseModel):
    key: str
    html: str
    status: str

# In-memory storage for demo purposes
widgets_db = {
    "sample-widget": {
        "html": """
        <div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px;">
            <h3>Sample Widget</h3>
            <p>This is a sample embeddable widget.</p>
        </div>
        """,
        "status": "active"
    },
    "weather-widget": {
        "html": """
        <div style="background: linear-gradient(135deg, #74b9ff, #0984e3); color: white; padding: 15px; border-radius: 10px; font-family: Arial, sans-serif;">
            <h3 style="margin: 0 0 10px 0;">Weather Widget</h3>
            <p style="margin: 0;">Current: 22°C, Sunny</p>
        </div>
        """,
        "status": "active"
    }
}

def validate_widget_key(key: str) -> bool:
    """Validate widget key format"""
    # Key should be alphanumeric with hyphens, 3-50 characters
    pattern = r'^[a-zA-Z0-9-]{3,50}$'
    return bool(re.match(pattern, key))

@app.get("/widget/{key}", response_class=HTMLResponse)
async def get_widget(
    key: str = Path(..., description="Widget key identifier", min_length=3, max_length=50)
):
    """
    Get embeddable widget by key
    
    Returns HTML content that can be embedded in other websites
    """
    
    # Input validation
    if not validate_widget_key(key):
        raise HTTPException(
            status_code=400, 
            detail="Invalid widget key format. Key must be 3-50 characters long and contain only letters, numbers, and hyphens."
        )
    
    # Check if widget exists
    if key not in widgets_db:
        raise HTTPException(
            status_code=404,
            detail=f"Widget with key '{key}' not found"
        )
    
    widget = widgets_db[key]
    
    # Check if widget is active
    if widget.get("status") != "active":
        raise HTTPException(
            status_code=410,
            detail=f"Widget '{key}' is not available"
        )
    
    # Return HTML content
    return HTMLResponse(
        content=widget["html"],
        headers={
            "Content-Type": "text/html; charset=utf-8",
            "Cache-Control": "public, max-age=300",  # Cache for 5 minutes
            "X-Frame-Options": "ALLOWALL",  # Allow embedding in iframes
            "Access-Control-Allow-Origin": "*"  # Allow cross-origin requests
        }
    )

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Widget API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "widgets_count": len(widgets_db)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)