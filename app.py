from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/api/sync', methods=['POST'])
def sync_data():
    """
    Synchronisiert lokale Daten mit Cloud
    """
    try:
        # Input validation
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        
        if data is None:
            return jsonify({
                'error': 'Invalid JSON payload'
            }), 400
        
        # Validate required fields
        if 'data' not in data:
            return jsonify({
                'error': 'Missing required field: data'
            }), 400
        
        if not isinstance(data['data'], list):
            return jsonify({
                'error': 'Field "data" must be an array'
            }), 400
        
        # Edge case: empty data array
        if len(data['data']) == 0:
            return jsonify({
                'message': 'No data to sync',
                'synced_count': 0,
                'status': 'success'
            }), 200
        
        # Edge case: data array too large
        if len(data['data']) > 1000:
            return jsonify({
                'error': 'Data array too large. Maximum 1000 items allowed'
            }), 400
        
        # Validate each data item
        for i, item in enumerate(data['data']):
            if not isinstance(item, dict):
                return jsonify({
                    'error': f'Data item at index {i} must be an object'
                }), 400
            
            if 'id' not in item:
                return jsonify({
                    'error': f'Data item at index {i} missing required field: id'
                }), 400
        
        # Simulate sync process
        synced_count = len(data['data'])
        
        # Log sync operation
        logging.info(f"Synced {synced_count} items to cloud")
        
        return jsonify({
            'message': 'Data synchronized successfully',
            'synced_count': synced_count,
            'status': 'success'
        }), 200
        
    except ValueError as e:
        # Handle JSON parsing errors
        return jsonify({
            'error': 'Invalid JSON format'
        }), 400
    
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Sync error: {str(e)}")
        return jsonify({
            'error': 'Internal server error during sync'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)