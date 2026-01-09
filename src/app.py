from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Vorteig-Methoden Daten
PREFERMENT_METHODS = [
    {
        "id": 1,
        "name": "Poolish",
        "description": "Flüssiger Vorteig mit gleichen Teilen Mehl und Wasser",
        "flour_ratio": 0.5,
        "water_ratio": 0.5,
        "yeast_ratio": 0.001,
        "fermentation_time": "12-16 Stunden",
        "temperature": "20-22°C"
    },
    {
        "id": 2,
        "name": "Biga",
        "description": "Fester italienischer Vorteig",
        "flour_ratio": 1.0,
        "water_ratio": 0.45,
        "yeast_ratio": 0.001,
        "fermentation_time": "12-24 Stunden",
        "temperature": "18-20°C"
    },
    {
        "id": 3,
        "name": "Pâte Fermentée",
        "description": "Alter Teig als Vorteig verwendet",
        "flour_ratio": 1.0,
        "water_ratio": 0.6,
        "yeast_ratio": 0.02,
        "fermentation_time": "8-24 Stunden",
        "temperature": "4-6°C"
    },
    {
        "id": 4,
        "name": "Sauerteig",
        "description": "Natürlich fermentierter Vorteig mit wilden Hefen",
        "flour_ratio": 1.0,
        "water_ratio": 1.0,
        "yeast_ratio": 0.0,
        "fermentation_time": "4-12 Stunden",
        "temperature": "24-28°C"
    }
]

@app.route('/api/preferment-methods', methods=['GET'])
def get_preferment_methods():
    try:
        # Input validation - keine Parameter erwartet für GET all
        # Erfolgreiche Antwort
        return jsonify({
            "success": True,
            "data": PREFERMENT_METHODS,
            "count": len(PREFERMENT_METHODS)
        }), 200
    
    except Exception as e:
        # Error handling für unerwartete Fehler
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
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
        "message": "The method is not allowed for the requested URL"
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