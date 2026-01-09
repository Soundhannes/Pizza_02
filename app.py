from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Pizza styles data
PIZZA_STYLES = [
    {
        "id": 1,
        "name": "Neapolitan",
        "description": "Traditional Italian pizza with thin crust, simple toppings, and high-temperature baking",
        "origin": "Naples, Italy",
        "characteristics": ["Thin crust", "Leopard spotting", "Simple ingredients", "Wood-fired oven"]
    },
    {
        "id": 2,
        "name": "New York Style",
        "description": "Large, thin-crust pizza that's crispy yet flexible, typically sold by the slice",
        "origin": "New York, USA",
        "characteristics": ["Large slices", "Thin but sturdy crust", "Foldable", "Generous cheese"]
    },
    {
        "id": 3,
        "name": "Chicago Deep Dish",
        "description": "Thick-crust pizza baked in a deep pan with cheese on bottom and sauce on top",
        "origin": "Chicago, USA",
        "characteristics": ["Deep dish", "Thick crust", "Cheese first", "Chunky tomato sauce on top"]
    },
    {
        "id": 4,
        "name": "Sicilian",
        "description": "Square-cut pizza with thick, airy crust and robust toppings",
        "origin": "Sicily, Italy",
        "characteristics": ["Square cut", "Thick focaccia-like crust", "Airy texture", "Robust flavors"]
    },
    {
        "id": 5,
        "name": "Detroit Style",
        "description": "Rectangular pizza with crispy, cheesy edges and sauce on top",
        "origin": "Detroit, USA",
        "characteristics": ["Rectangular shape", "Crispy edges", "Brick cheese", "Sauce on top"]
    }
]

@app.route('/api/pizza-styles', methods=['GET'])
def get_pizza_styles():
    try:
        # Input validation - GET requests typically don't have body data to validate
        # But we can validate query parameters if any are expected in the future
        
        # Return all pizza styles
        return jsonify({
            "success": True,
            "data": PIZZA_STYLES,
            "count": len(PIZZA_STYLES)
        }), 200
        
    except Exception as e:
        # Error handling for edge cases
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": "An unexpected error occurred while fetching pizza styles"
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Not found",
        "message": "The requested resource was not found"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": "Method not allowed",
        "message": "The requested method is not allowed for this endpoint"
    }), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)