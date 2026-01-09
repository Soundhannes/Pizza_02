from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError
import uuid
from datetime import datetime

app = Flask(__name__)

# In-memory storage for widgets (in production, use a database)
widgets = {}

class WidgetSchema(Schema):
    name = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)
    type = fields.Str(required=True, validate=lambda x: x in ['chart', 'table', 'metric', 'text'])
    config = fields.Dict(required=True)
    position = fields.Dict(required=False, missing={})
    enabled = fields.Bool(required=False, missing=True)

widget_schema = WidgetSchema()

@app.route('/api/widgets', methods=['POST'])
def create_widget():
    try:
        # Validate JSON content type
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json'
            }), 400
        
        # Get JSON data
        json_data = request.get_json()
        
        if json_data is None:
            return jsonify({
                'error': 'Invalid JSON data'
            }), 400
        
        # Validate input data
        try:
            validated_data = widget_schema.load(json_data)
        except ValidationError as err:
            return jsonify({
                'error': 'Validation failed',
                'details': err.messages
            }), 400
        
        # Generate unique ID and timestamps
        widget_id = str(uuid.uuid4())
        current_time = datetime.utcnow().isoformat()
        
        # Create widget object
        widget = {
            'id': widget_id,
            'name': validated_data['name'].strip(),
            'type': validated_data['type'],
            'config': validated_data['config'],
            'position': validated_data['position'],
            'enabled': validated_data['enabled'],
            'created_at': current_time,
            'updated_at': current_time
        }
        
        # Store widget
        widgets[widget_id] = widget
        
        # Return created widget
        return jsonify(widget), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    app.run(debug=True)