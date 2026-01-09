from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)

class CalculateRequestSchema(Schema):
    base_amount = fields.Float(required=True, validate=lambda x: x > 0)
    target_amount = fields.Float(required=True, validate=lambda x: x > 0)
    ingredients = fields.Dict(
        keys=fields.Str(),
        values=fields.Float(validate=lambda x: x >= 0),
        required=True,
        validate=lambda x: len(x) > 0
    )

@app.route('/api/calculate', methods=['POST'])
def calculate():
    schema = CalculateRequestSchema()
    
    try:
        # Input validation
        data = schema.load(request.json or {})
    except ValidationError as err:
        return jsonify({'error': 'Invalid input', 'details': err.messages}), 400
    except Exception:
        return jsonify({'error': 'Invalid JSON format'}), 400
    
    try:
        base_amount = data['base_amount']
        target_amount = data['target_amount']
        ingredients = data['ingredients']
        
        # Calculate scaling factor
        scaling_factor = target_amount / base_amount
        
        # Calculate scaled ingredients
        scaled_ingredients = {}
        for ingredient, amount in ingredients.items():
            scaled_ingredients[ingredient] = round(amount * scaling_factor, 2)
        
        return jsonify({
            'base_amount': base_amount,
            'target_amount': target_amount,
            'scaling_factor': round(scaling_factor, 4),
            'scaled_ingredients': scaled_ingredients
        }), 200
        
    except ZeroDivisionError:
        return jsonify({'error': 'Base amount cannot be zero'}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)