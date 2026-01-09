from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Konfiguration
RECIPES_DIR = 'data/recipes'

def ensure_recipes_dir():
    """Stellt sicher, dass das Rezepte-Verzeichnis existiert"""
    if not os.path.exists(RECIPES_DIR):
        os.makedirs(RECIPES_DIR)

def load_recipe(filename):
    """Lädt ein einzelnes Rezept aus einer Datei"""
    try:
        filepath = os.path.join(RECIPES_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            recipe = json.load(f)
            # Füge die ID basierend auf dem Dateinamen hinzu
            recipe['id'] = filename.replace('.json', '')
            return recipe
    except (json.JSONDecodeError, FileNotFoundError, KeyError):
        return None

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """
    GET /api/recipes - Lädt gespeicherte Rezepte
    
    Query Parameter:
    - limit: Maximale Anzahl der Rezepte (optional, Standard: alle)
    - offset: Anzahl der zu überspringenden Rezepte (optional, Standard: 0)
    """
    try:
        # Input validation
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int, default=0)
        
        # Validierung der Parameter
        if limit is not None and limit < 0:
            return jsonify({
                'error': 'Invalid limit parameter',
                'message': 'Limit must be a non-negative integer'
            }), 400
            
        if offset < 0:
            return jsonify({
                'error': 'Invalid offset parameter',
                'message': 'Offset must be a non-negative integer'
            }), 400
        
        # Stelle sicher, dass das Verzeichnis existiert
        ensure_recipes_dir()
        
        # Lade alle Rezepte
        recipes = []
        
        try:
            recipe_files = [f for f in os.listdir(RECIPES_DIR) if f.endswith('.json')]
        except OSError:
            # Verzeichnis existiert nicht oder ist nicht lesbar
            return jsonify({
                'recipes': [],
                'total': 0,
                'offset': offset,
                'limit': limit
            })
        
        # Sortiere Dateien für konsistente Reihenfolge
        recipe_files.sort()
        
        for filename in recipe_files:
            recipe = load_recipe(filename)
            if recipe is not None:
                recipes.append(recipe)
        
        # Anwenden von offset und limit
        total_recipes = len(recipes)
        
        if offset >= total_recipes and total_recipes > 0:
            return jsonify({
                'error': 'Invalid offset parameter',
                'message': f'Offset {offset} is greater than total recipes {total_recipes}'
            }), 400
        
        # Slice für Pagination
        start_index = offset
        end_index = start_index + limit if limit is not None else len(recipes)
        paginated_recipes = recipes[start_index:end_index]
        
        return jsonify({
            'recipes': paginated_recipes,
            'total': total_recipes,
            'offset': offset,
            'limit': limit,
            'count': len(paginated_recipes)
        })
        
    except Exception as e:
        # Allgemeine Fehlerbehandlung
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred while loading recipes'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not found',
        'message': 'The requested resource was not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)