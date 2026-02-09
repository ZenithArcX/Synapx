"""
Minimal Flask API server for the claims processing agent.
Serves the React frontend and exposes a file upload API.
"""
import os
import tempfile
from typing import Dict, Any

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from agent import ClaimsProcessingAgent

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR)

# Enable CORS for Render deployment
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

agent = ClaimsProcessingAgent()


@app.get("/")
def index() -> Any:
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/frontend/<path:filename>")
def frontend_assets(filename: str) -> Any:
    return send_from_directory(FRONTEND_DIR, filename)


@app.post("/api/claims/process")
def process_claim() -> Any:
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    upload = request.files["file"]
    if not upload.filename:
        return jsonify({"error": "Empty filename"}), 400

    _, ext = os.path.splitext(upload.filename)
    ext = ext.lower()
    if ext not in [".pdf", ".txt"]:
        return jsonify({"error": "Only .pdf and .txt files are supported"}), 400

    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
            upload.save(temp_file.name)
            temp_file_path = temp_file.name

        result: Dict[str, Any] = agent.process_claim(temp_file_path)
        return jsonify(result)
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@app.post("/api/claims/process-form")
def process_form() -> Any:
    """Process manually entered claim data from the form."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Format the data as if it came from extraction
        extracted_fields = {
            "policy_number": data.get("policy_number", ""),
            "policyholder_name": data.get("policyholder_name", ""),
            "incident_date": data.get("incident_date", ""),
            "incident_location": data.get("incident_location", ""),
            "claim_type": data.get("claim_type", ""),
            "estimated_damage": data.get("estimated_damage", ""),
            "vehicle_vin": data.get("vehicle_vin", ""),
            "accident_description": data.get("accident_description", ""),
        }

        # Validate mandatory fields
        missing_fields = agent.extractor.validate_fields(extracted_fields)

        # Check for fraud in description
        fraud_indicators = agent.extractor.check_for_fraud_indicators(
            data.get("accident_description", "")
        )

        # Convert damage to numeric for routing
        damage_str = data.get("estimated_damage", "0")
        try:
            extracted_fields["estimated_damage_value"] = float(damage_str)
        except ValueError:
            extracted_fields["estimated_damage_value"] = 0

        # Determine route
        routing = agent.router.determine_route(
            extracted_fields, missing_fields, fraud_indicators
        )

        result = {
            "status": "SUCCESS",
            "extractedFields": extracted_fields,
            "missingFields": missing_fields,
            "fraudIndicators": fraud_indicators,
            "recommendedRoute": routing["recommendedRoute"],
            "reasoning": routing["reasoning"],
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Use environment variables for deployment
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False") == "True"
    
    app.run(host=host, port=port, debug=debug)
