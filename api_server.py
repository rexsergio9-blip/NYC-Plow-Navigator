from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/api/route', methods=['POST'])
def get_route_recommendation():
    data = request.json
    start = data.get('start', 'Times Square')
    end = data.get('end', 'Central Park')
    
    response = {
        "recommended_route": f"From {start} to {end}: head north on Broadway, then east on 59th St.",
        "reasoning": "Broadway is recently plowed (30m ago) while alternative routes are still covered in snow.",
        "alternative_route": "7th Ave to 57th St.",
        "risk_score": 2,
        "estimated_time": "15 mins",
        "warnings": ["Monitor road conditions."]
    }
    return jsonify({"success": True, "recommendation": response})

@app.route('/api/health')
def health(): return jsonify({"status": "running"})

if __name__ == '__main__':
    app.run(port=5001, host='127.0.0.1')
