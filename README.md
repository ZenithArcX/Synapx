# Autonomous Insurance Claims Processing Agent

A lightweight, intelligent agent designed to extract key fields from FNOL (First Notice of Loss) documents, validate completeness, identify inconsistencies, and automatically route claims to appropriate processing queues.

## Assessment Overview

This solution was developed for Synapx's Junior Software Developer assessment. The agent demonstrates capabilities in:

- **Document Processing**: Extract structured data from unstructured PDF and text documents
- **Field Extraction**: Identify and extract 15+ key insurance claim fields using pattern matching
- **Data Validation**: Detect missing mandatory fields and inconsistent data
- **Intelligent Routing**: Classify claims and route to appropriate workflows based on configurable business rules
- **Fraud Detection**: Flag potential fraud indicators for investigation

## Key Features

### 1. **Multi-Format Support**
- PDF documents (using pdfplumber)
- Text-based documents
- Batch processing of multiple files

### 2. **Comprehensive Field Extraction**

Extracts the following field categories:

**Policy Information:**
- Policy Number
- Policyholder Name
- Effective Dates

**Incident Information:**
- Date, Time, Location
- Detailed Description

**Involved Parties:**
- Claimant, Third Parties
- Contact Details

**Asset Details:**
- Asset Type, ID
- Estimated Damage

**Mandatory Fields:**
- Claim Type
- Attachments
- Initial Estimate

### 3. **Intelligent Routing Engine**

Routes claims based on these rules (in priority order):

```
Rule 1: Missing Mandatory Fields
   → Route: MANUAL_REVIEW
   → Action: Human review required

Rule 2: Fraud Indicators Detected
   → Keywords: "fraud", "inconsistent", "staged", "suspicious", "falsified"
   → Route: INVESTIGATION_FLAG
   → Action: Investigation team review

Rule 3: Injury Claims
   → Claim Type: Contains "injury", "bodily", "personal"
   → Route: SPECIALIST_QUEUE
   → Action: Medical specialist review

Rule 4: Damage Amount < $25,000
   → Route: FAST_TRACK
   → Action: Expedited processing

Rule 5: Damage Amount ≥ $25,000
   → Route: STANDARD_REVIEW
   → Action: Standard review workflow
```

### 4. **JSON Output Format**

```json
{
  "status": "SUCCESS",
  "document_path": "path/to/document.pdf",
  "extractedFields": {
    "policy_number": "POL-2024-001234",
    "policyholder_name": "John Michael Thompson",
    "incident_date": "02/03/2026",
    "incident_location": "Intersection of Oak Lane and Maple Street, Springfield, IL 62701",
    "claim_type": "Auto Collision",
    "estimated_damage": "$8,750.00",
    ...
  },
  "missingFields": [],
  "fraudIndicators": [],
  "recommendedRoute": "FAST_TRACK",
  "reasoning": "Low damage amount ($8,750.00 < $25,000). Eligible for expedited processing."
}
```

## Project Structure

```
insurance-claims-agent/
├── agent.py                  # Main entry point
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── src/
│   ├── __init__.py
│   ├── pdf_parser.py         # PDF and text file parsing
│   ├── field_extractor.py    # Field extraction and validation
│   └── routing_engine.py     # Claim routing logic
├── sample_documents/         # Test claim documents
│   ├── claim_sample_001.txt  # Standard collision claim
│   ├── claim_sample_002.txt  # High-value claim
│   ├── claim_sample_003.txt  # Fraud flag scenario
│   ├── claim_sample_004.txt  # Injury claim
│   └── claim_sample_005.txt  # Incomplete/missing fields
└── output/                   # Processing results
    └── claims_processing_results.json
```

## Installation

### Prerequisites
- Python 3.8 or higher
- venv module support

### Setup Steps (Professional Virtual Environment Approach)

**Important:** Always use a virtual environment to keep your system clean and avoid breaking dependencies.

1. **Install venv support (one-time setup)**
```bash
sudo apt install python3-venv python3-full -y
```

2. **Navigate to the project**
```bash
cd /mnt/data/projects/SYNAPX/insurance-claims-agent
```

3. **Create a virtual environment**
```bash
python3 -m venv venv
```

4. **Activate the virtual environment**
```bash
source venv/bin/activate
```
You should see `(venv)` prefix in your terminal prompt.

5. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Deactivating the Environment
When you're done working on the project:
```bash
deactivate
```

## Usage

### Process a Single Document

```bash
python agent.py -i sample_documents/claim_sample_001.txt
```

### Process Multiple Documents

```bash
python agent.py -i sample_documents -o output/results.json
```

### Command-Line Options

```
-i, --input      (required) Path to input file or directory
-o, --output     (optional) Output JSON path (default: output/claims_processing_results.json)
```

### Example Usage

```bash
# Process all samples and save results
python agent.py -i sample_documents -o output/processing_results.json

# Process specific file
python agent.py -i sample_documents/claim_sample_001.txt

# Custom output location
python agent.py -i sample_documents -o my_results.json
```

## Technical Approach

### 1. **Document Parsing**
- Uses `pdfplumber` for PDF extraction
- Native file handling for TXT files
- Converts unstructured text to readable format

### 2. **Field Extraction**
- Regex pattern matching for field identification
- Case-insensitive matching to handle variations
- Multi-line pattern support for complex fields
- Error handling for malformed documents

### 3. **Data Validation**
- Mandatory field checklist
- Missing field identification
- Type conversion for numeric fields (damage amounts)
- Fraud keyword detection

### 4. **Routing Logic**
- Rule-based decision engine
- Priority-ordered evaluation
- Configurable thresholds ($25,000 damage limit)
- Detailed reasoning for each routing decision

## Sample Test Results

### Sample 1: Standard Collision Claim
```
Route: FAST_TRACK
Reason: Low damage amount ($8,750.00 < $25,000). Eligible for expedited processing.
```

### Sample 2: High-Value Claim
```
Route: STANDARD_REVIEW
Reason: High damage amount ($45,200.00 >= $25,000). Requires standard review.
```

### Sample 3: Fraud Investigation Flag
```
Route: INVESTIGATION_FLAG
Reason: Potential fraud indicators detected: inconsistent, staged
```

### Sample 4: Injury Claim
```
Route: SPECIALIST_QUEUE
Reason: Claim type requires specialist handling (injury/bodily harm involved)
```

### Sample 5: Incomplete Information
```
Route: MANUAL_REVIEW
Reason: Missing mandatory fields: policy_number, incident_time
```

## Running the Assessment

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run processing on all sample documents
python agent.py -i sample_documents

# View results
cat output/claims_processing_results.json
```

### Verification

The solution includes 5 diverse sample documents testing:
1. ✅ Standard claim extraction and fast-track routing
2. ✅ High-value claim detection for standard review
3. ✅ Fraud indicator detection
4. ✅ Injury claim specialist routing
5. ✅ Missing field validation and manual review

## Architecture & Design Decisions

### Modularity
- **DocumentParser**: Handles file format conversion
- **FieldExtractor**: Manages data extraction and validation
- **RoutingEngine**: Implements business logic
- **ClaimsProcessingAgent**: Orchestrates the workflow

### Extensibility
The agent is designed for easy extension:

```python
# Add new field patterns
FIELD_PATTERNS = {
    "custom_field": r"pattern_here"
}

# Add routing rules
if custom_condition:
    route = "CUSTOM_ROUTE"
    reasoning = "Custom logic applied"

# Add fraud indicators
fraud_keywords = ["new_keyword1", "new_keyword2"]
```

### Error Handling
- Graceful document parsing failures
- Missing field detection
- Invalid data type handling
- File I/O error management

## Limitations & Future Enhancements

### Current Limitations
1. Pattern-based extraction (no ML/NLP engines)
2. English-only document support
3. No OCR for scanned documents
4. Basic fraud detection (keyword-based)

### Potential Enhancements
1. **AI Integration**: Use LLMs for semantic field extraction
2. **Advanced NLP**: Named entity recognition for better extraction
3. **OCR Support**: Handle scanned PDF documents
4. **Machine Learning**: Train models for fraud detection
5. **Database Integration**: Store results in production database
6. **API Layer**: REST API for external integrations
7. **Document Verification**: Validate document authenticity
8. **Performance Optimization**: Batch processing optimization
9. **Logging & Monitoring**: Comprehensive audit trails
10. **Web Dashboard**: Interactive claim processing interface

## Dependencies

- **pdfplumber** (0.10.3) - PDF text extraction
- **PyPDF2** (3.0.1) - PDF manipulation
- **python-dotenv** (1.0.0) - Environment configuration

## Testing

### Run Sample Processing
```bash
python agent.py -i sample_documents -o output/test_results.json
```

### Expected Output
- 5 JSON result objects
- Routes: FAST_TRACK (1), STANDARD_REVIEW (1), INVESTIGATION_FLAG (1), SPECIALIST_QUEUE (1), MANUAL_REVIEW (1)
- All mandatory fields validated
- Fraud indicators properly detected

## Submission Components

✅ **Source Code**
- Modular Python agent with 4 core modules
- Clean, documented code
- Comprehensive error handling

✅ **Documentation**
- This README with complete usage instructions
- Code comments and docstrings
- Sample documents with clear scenarios

✅ **Sample Data**
- 5 diverse test documents covering all routing scenarios
- Realistic insurance claim data
- Edge cases and error conditions

✅ **Output Format**
- JSON structure matching requirements
- Complete field extraction
- Detailed routing reasoning

## Author & Notes

Developed for: **Synapx Junior Software Developer Assessment**\
Date: February 2026\
Status: ✅ Complete and Ready for Evaluation

## Contact & Support

For questions about this assessment solution, please refer to the code documentation and sample outputs provided.

---

**Assessment Deadline:** February 9, 2026
