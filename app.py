from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory storage for recipes
recipes = []

def validate_recipe_data(data):
    """Validate recipe input data"""
    errors = []
    
    if not data:
        errors.append("Request body is required")
        return errors
    
    # Required fields
    required_fields = ['name', 'ingredients', 'instructions']
    for field in required_fields:
        if field not in data:
            errors.append(f"Field '{field}' is required")
        elif not data[field] or (isinstance(data[field], str) and not data[field].strip()):
            errors.append(f"Field '{field}' cannot be empty")
    
    # Validate ingredients
    if 'ingredients' in data:
        if not isinstance(data['ingredients'], list):
            errors.append("Field 'ingredients' must be a list")
        elif len(data['ingredients']) == 0:
            errors.append("At least one ingredient is required")
        else:
            for i, ingredient in enumerate(data['ingredients']):
                if not isinstance(ingredient, str) or not ingredient.strip():
                    errors.append(f"Ingredient at index {i} must be a non-empty string")
    
    # Validate instructions
    if 'instructions' in data:
        if not isinstance(data['instructions'], list):
            errors.append("Field 'instructions' must be a list")
        elif len(data['instructions']) == 0:
            errors.append("At least one instruction is required")
        else:
            for i, instruction in enumerate(data['instructions']):
                if not isinstance(instruction, str) or not instruction.strip():
                    errors.append(f"Instruction at index {i} must be a non-empty string")
    
    # Validate name
    if 'name' in data and isinstance(data['name'], str):
        if len(data['name'].strip()) > 200:
            errors.append("Recipe name cannot exceed 200 characters")
    
    # Validate optional fields
    if 'prep_time' in data:
        if not isinstance(data['prep_time'], int) or data['prep_time'] < 0:
            errors.append("Field 'prep_time' must be a non-negative integer")
    
    if 'cook_time' in data:
        if not isinstance(data['cook_time'], int) or data['cook_time'] < 0:
            errors.append("Field 'cook_time' must be a non-negative integer")
    
    if 'servings' in data:
        if not isinstance(data['servings'], int) or data['servings'] <= 0:
            errors.append("Field 'servings' must be a positive integer")
    
    return errors

@app.route('/api/recipes', methods=['POST'])
def create_recipe():
    """Create a new recipe"""
    try:
        # Check content type
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        
        # Validate input data
        validation_errors = validate_recipe_data(data)
        if validation_errors:
            return jsonify({
                'error': 'Validation failed',
                'details': validation_errors
            }), 400
        
        # Create new recipe
        recipe = {
            'id': str(uuid.uuid4()),
            'name': data['name'].strip(),
            'ingredients': [ingredient.strip() for ingredient in data['ingredients']],
            'instructions': [instruction.strip() for instruction in data['instructions']],
            'prep_time': data.get('prep_time'),
            'cook_time': data.get('cook_time'),
            'servings': data.get('servings'),
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Store recipe
        recipes.append(recipe)
        
        return jsonify(recipe), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)