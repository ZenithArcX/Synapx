# Quick Start Guide

## One-Command Setup (Recommended)

```bash
# 1. Navigate to project
cd /mnt/data/projects/SYNAPX/insurance-claims-agent

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate it
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

Your terminal should now show `(venv)` prefix.

---

## Run the Agent

### Process All Sample Documents
```bash
python agent.py -i sample_documents
```

### Process Specific File
```bash
python agent.py -i sample_documents/claim_sample_001.txt
```

### Custom Output Location
```bash
python agent.py -i sample_documents -o my_results.json
```

---

## View Results

```bash
# Pretty-print the JSON results
cat output/claims_processing_results.json | python3 -m json.tool

# Or use less for large files
cat output/claims_processing_results.json | python3 -m json.tool | less
```

---

## What the Agent Does

✅ **Extracts** 15+ fields from claim documents  
✅ **Validates** mandatory field presence  
✅ **Detects** fraud indicators  
✅ **Routes** claims intelligently based on rules:
- Low damage (<$25k) → **FAST_TRACK**
- High damage (≥$25k) → **STANDARD_REVIEW**
- Missing fields → **MANUAL_REVIEW**
- Fraud keywords → **INVESTIGATION_FLAG**
- Injury claims → **SPECIALIST_QUEUE**

---

## Sample Documents Included

| File | Scenario | Expected Route |
|------|----------|-----------------|
| claim_sample_001.txt | Standard collision ($8.7k) | FAST_TRACK |
| claim_sample_002.txt | Hit & run ($45.2k) | STANDARD_REVIEW |
| claim_sample_003.txt | Suspicious fire | INVESTIGATION_FLAG |
| claim_sample_004.txt | Bodily injury involved | SPECIALIST_QUEUE |
| claim_sample_005.txt | Missing information | MANUAL_REVIEW |

---

## File Structure

```
insurance-claims-agent/
├── agent.py                 # Main entry point
├── requirements.txt         # Dependencies
├── README.md               # Full documentation
├── QUICKSTART.md           # This file
├── setup.sh                # Automated setup
├── src/
│   ├── pdf_parser.py       # PDF/TXT parsing
│   ├── field_extractor.py  # Field extraction
│   └── routing_engine.py   # Routing logic
├── sample_documents/       # 5 test cases
└── output/                 # Results folder
```

---

## Important: Keep Virtual Environment Active

Whenever you return to this project:

```bash
cd /mnt/data/projects/SYNAPX/insurance-claims-agent
source venv/bin/activate
```

To deactivate when done:
```bash
deactivate
```

---

## Troubleshooting

**Q: "ModuleNotFoundError: No module named 'pdfplumber'"**  
A: You forgot to activate venv: `source venv/bin/activate`

**Q: "command not found: python3"**  
A: Ensure Python 3.8+ is installed: `python3 --version`

**Q: Permission denied on setup.sh**  
A: Make it executable: `chmod +x setup.sh`

---

## Key Features

### 🎯 Smart Field Extraction
Uses regex patterns to find fields even in unstructured documents

### 🚦 Intelligent Routing
Priority-based rules ensuring claims go to the right queue

### 🔍 Fraud Detection
Keyword-based detection for suspicious indicators

### 📊 JSON Output
Structured results for integration with other systems

### 🔐 Modular Design
Easy to extend: add fields, routing rules, or detectors

---

## Next Steps

1. ✅ Set up virtual environment (already done if following above)
2. ✅ Install dependencies (already done)
3. ✅ Run agent on sample data
4. 📄 Review output JSON results
5. 🚀 Integrate into your workflow
6. 📈 Add more sample documents as needed

---

**Status:** ✅ Ready to use  
**Date:** February 2026  
**Assessment:** Synapx Junior Software Developer
