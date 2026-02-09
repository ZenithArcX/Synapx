# Frontend and API Integration Guide

This guide explains how the React UI connects to the Python claims agent, and how each Python module is used behind the API.

## Overview

We added two pieces:

1. A React frontend with **two tabs** (file upload + manual form entry)
2. A lightweight Flask API with **two endpoints**

The frontend can either:
- Upload a claim document, or
- Manually fill in claim details via a form

Both routes call the Python agent and return the same JSON output.

## Two Ways to Process Claims

### Option 1: Upload Document
1. User selects PDF/TXT file
2. Uploads to `/api/claims/process`
3. API extracts fields, validates, routes
4. Returns JSON result

### Option 2: Manual Entry
1. User fills form fields
2. Submits to `/api/claims/process-form`
3. API validates, routes using form data
4. Returns JSON result

## Frontend Architecture (React)

### Files

- [frontend/index.html](../frontend/index.html)
- [frontend/app.js](../frontend/app.js)
- [frontend/styles.css](../frontend/styles.css)

### Tab Components

**Upload Document Tab**
- File input for PDF/TXT
- Submit button
- Error handling
- Result display

**Manual Entry Tab**
- Form fields for claim data:
  - Policy Number (required)
  - Policyholder Name (required)
  - Incident Date (optional)
  - Incident Location (optional)
  - Claim Type (dropdown)
  - Estimated Damage (currency)
  - Vehicle VIN (optional)
  - Accident Description (textarea)
- Submit button
- Form validation
- Result display

### Frontend Code Flow

**File Upload:**
```javascript
const formData = new FormData();
formData.append("file", file);

const response = await fetch("/api/claims/process", {
  method: "POST",
  body: formData,
});

const data = await response.json();
setResult(data);
```

**Form submission:**
```javascript
const response = await fetch("/api/claims/process-form", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(formData),
});

const data = await response.json();
setResult(data);
```

### Why This Is Simple

- Uses only React and ReactDOM from CDN.
- No build tooling, no bundlers, no extra libraries.
- All code is in a single file (`app.js`).

## API Integration (Flask)

### Files

- [api_server.py](../api_server.py)

### Endpoints

#### 1. `POST /api/claims/process`
- Accepts file upload (PDF or TXT)
- Saves to temporary file
- Calls `ClaimsProcessingAgent.process_claim()`
- Returns JSON result

#### 2. `POST /api/claims/process-form`
- Accepts JSON form data
- Validates mandatory fields
- Calls extraction/routing logic
- Returns JSON result

### API Code Flow

**File Upload Endpoint:**
```python
upload = request.files["file"]

with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
    upload.save(temp_file.name)
    temp_file_path = temp_file.name

result = agent.process_claim(temp_file_path)
return jsonify(result)
```

**Form Endpoint:**
```python
data = request.get_json()

extracted_fields = {
    "policy_number": data.get("policy_number", ""),
    "policyholder_name": data.get("policyholder_name", ""),
    # ... other fields
}

missing_fields = agent.extractor.validate_fields(extracted_fields)
fraud_indicators = agent.extractor.check_for_fraud_indicators(
    data.get("accident_description", "")
)

routing = agent.router.determine_route(
    extracted_fields, missing_fields, fraud_indicators
)

return jsonify(result)
```

## How the API Uses the Python Modules

Both endpoints use the same pipeline as the CLI.

```
api_server.py
   ↓
   ├─ /api/claims/process (file upload)
   │   └─ ClaimsProcessingAgent.process_claim()
   │       ├─ DocumentParser (src/pdf_parser.py)
   │       ├─ FieldExtractor (src/field_extractor.py)
   │       └─ RoutingEngine (src/routing_engine.py)
   │
   └─ /api/claims/process-form (form entry)
       └─ Direct calls to:
           ├─ FieldExtractor.validate_fields()
           ├─ FieldExtractor.check_for_fraud_indicators()
           └─ RoutingEngine.determine_route()
```

### Module Responsibilities

- [agent.py](../agent.py)
  - Orchestrates the pipeline
  - Combines parsing, extraction, validation, and routing

- [src/pdf_parser.py](../src/pdf_parser.py)
  - Reads PDF/TXT files
  - Returns raw text

- [src/field_extractor.py](../src/field_extractor.py)
  - Extracts structured fields with regex
  - Validates mandatory fields
  - Detects fraud keywords

- [src/routing_engine.py](../src/routing_engine.py)
  - Applies business rules
  - Selects routing queue
  - Generates reasoning

## Running the Frontend with API

### Step 1: Install dependencies

```bash
cd insurance-claims-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Start the API server

```bash
python api_server.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 3: Open the UI

Visit:

```
http://127.0.0.1:5000
```

The UI and API share the same host and port, so there is no CORS setup needed.

## Request and Response Examples

### Request 1: File Upload

- Method: `POST`
- URL: `/api/claims/process`
- Body: `multipart/form-data` with `file`

### Request 2: Form Entry

```json
POST /api/claims/process-form
Content-Type: application/json

{
  "policy_number": "POL-2024-001234",
  "policyholder_name": "John Doe",
  "incident_date": "2026-02-10",
  "incident_location": "Main Street, Springfield",
  "claim_type": "Auto Collision",
  "estimated_damage": "8750",
  "vehicle_vin": "1HGBH41JXMN109186",
  "accident_description": "Two-vehicle collision at intersection..."
}
```

### Response (Both endpoints return same format)

```json
{
  "status": "SUCCESS",
  "extractedFields": {
    "policy_number": "POL-2024-001234",
    "policyholder_name": "John Doe",
    "incident_date": "2026-02-10",
    "incident_location": "Main Street, Springfield",
    "claim_type": "Auto Collision",
    "estimated_damage": "8750",
    "estimated_damage_value": 8750.0,
    "vehicle_vin": "1HGBH41JXMN109186"
  },
  "missingFields": [],
  "fraudIndicators": [],
  "recommendedRoute": "FAST_TRACK",
  "reasoning": "Low damage amount ($8,750.00 < $25,000). Eligible for expedited processing."
}
```

## Form Validation

### Frontend Validation
- Checks for required fields (Policy#, Policyholder Name)
- Shows error message if missing

### Backend Validation
- Double-checks mandatory fields
- Detects placeholder values
- Validates data format

## Result Display

The UI displays results in two ways:

1. **Summary View** (always shown)
   - Recommended route
   - Reasoning
   - Missing fields (if any)
   - Fraud indicators (if any)

2. **Detailed View** (expandable)
   - Full JSON response
   - All extracted fields
   - All validation results

## Optional Enhancements

- Add a results table instead of JSON text
- Add drag-and-drop file upload
- Add a history list of processed claims
- Add a "Download JSON" button
- Add batch processing (multiple files)
- Add user authentication
- Add database storage of results

## Troubleshooting

- **UI loads but upload fails**: Check that `api_server.py` is running
- **ModuleNotFoundError: flask**: Run `pip install Flask==3.0.2`
- **Only .pdf and .txt files supported**: Check your file type
- **Form shows "Missing fields"**: Fill in Policy Number and Policyholder Name
- **CORS error**: Should not happen—both UI and API on same origin
