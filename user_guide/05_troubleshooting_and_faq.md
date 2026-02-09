# Troubleshooting & FAQ

## Quick Troubleshooting

### Problem: Module Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'pdfplumber'
```

**Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| Virtual environment not activated | `source venv/bin/activate` |
| Dependencies not installed | `pip install -r requirements.txt` |
| Wrong Python version | Ensure Python 3.8+: `python3 --version` |
| Multiple Python installations | Use full path: `/usr/bin/python3 -m venv venv` |

**Step-by-step fix:**
```bash
# 1. Verify virtual environment
which python3
# Should show: .../insurance-claims-agent/venv/bin/python3

# 2. If not, activate
source venv/bin/activate

# 3. Verify installation
pip list | grep pdfplumber
# Should show: pdfplumber 0.10.3

# 4. If missing, install
pip install -r requirements.txt

# 5. Test import
python3 -c "import pdfplumber; print('✓ OK')"
```

---

### Problem: File Not Found

**Error:**
```
FileNotFoundError: Document not found: /path/to/file.pdf
```

**Solutions:**

1. **Check file exists:**
   ```bash
   ls -la sample_documents/
   # Should show: claim_sample_001.txt, claim_sample_002.txt, etc.
   ```

2. **Use correct path:**
   ```bash
   # Relative path (current directory)
   python agent.py -i sample_documents/claim_sample_001.txt
   
   # Absolute path
   python agent.py -i /mnt/data/projects/SYNAPX/insurance-claims-agent/sample_documents/claim_sample_001.txt
   ```

3. **Check file permissions:**
   ```bash
   ls -la sample_documents/claim_sample_001.txt
   # Should be readable (r-- permission)
   
   # Fix permissions if needed
   chmod 644 sample_documents/claim_sample_001.txt
   ```

---

### Problem: Permission Denied

**Error:**
```
PermissionError: [Errno 13] Permission denied: 'output/results.json'
```

**Solutions:**

1. **Check output directory exists:**
   ```bash
   mkdir -p output
   ```

2. **Fix directory permissions:**
   ```bash
   chmod 755 output
   chmod 644 output/results.json  # If file exists
   ```

3. **Check file ownership:**
   ```bash
   ls -la output/
   # Fix ownership if needed
   chown $USER:$USER output
   ```

---

### Problem: PDF Extraction Issues

**Error:**
```
Exception: Error reading PDF file: [some error]
```

**Common Causes & Solutions:**

| Issue | Cause | Solution |
|-------|-------|----------|
| Corrupted PDF | File damage | Try opening in PDF reader first |
| Scanned PDF | No text layer | Would need OCR (not supported yet) |
| Encrypted PDF | Password protected | Remove encryption first |
| Very large PDF | Memory issue | Increase system RAM or split PDF |

**Test PDF parsing:**
```bash
python3 << 'EOF'
from src.pdf_parser import DocumentParser

parser = DocumentParser()
try:
    text = parser.parse_document("sample_documents/test.pdf")
    print("✓ PDF parsed successfully")
    print(f"Extracted {len(text)} characters")
except Exception as e:
    print(f"✗ Error: {e}")
EOF
```

---

## FAQ

### Q1: What Python versions are supported?

**A:** Python 3.8 or higher.

**Check your version:**
```bash
python3 --version
# If Python 3.11 or higher, you're good
```

**Install specific version:**
```bash
sudo apt install python3.9  # Ubuntu example
python3.9 -m venv venv
```

---

### Q2: Can I run this on Windows or macOS?

**A:** Yes! The code is cross-platform.

**Windows Setup:**
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows Command Prompt)
venv\Scripts\activate

# Or PowerShell
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

**macOS Setup:**
```bash
# Install Python if needed
brew install python3

# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Install
pip install -r requirements.txt
```

---

### Q3: How do I modify the fraud detection keywords?

**A:** Edit the `FRAUD_KEYWORDS` in `src/field_extractor.py`:

```python
# In field_extractor.py, class FieldExtractor

def check_for_fraud_indicators(self, text: str) -> List[str]:
    """Check for fraud-related keywords in document"""
    # MODIFY THIS LIST
    fraud_keywords = [
        "fraud",           # Keep existing
        "inconsistent",
        "staged",
        "suspicious",
        "falsified",
        "NEW_KEYWORD",     # Add new keywords here
        "ANOTHER_KEYWORD"
    ]
    # ... rest of code
```

**Or use environment variable:**
```bash
# In .env file
FRAUD_KEYWORDS=fraud,inconsistent,staged,suspicious,new_keyword
```

---

### Q4: How do I change the damage threshold?

**A:** Edit `FAST_TRACK_THRESHOLD` in `src/routing_engine.py`:

```python
# In routing_engine.py, class RoutingEngine

class RoutingEngine:
    """Route claims to appropriate queues based on business rules"""
    
    # Change this value (currently $25,000)
    FAST_TRACK_THRESHOLD = 50000  # Now $50,000 instead
```

**Or use environment variable:**
```bash
# In .env file
DAMAGE_THRESHOLD=50000
```

**Then update code to use it:**
```python
from dotenv import load_dotenv
import os

load_dotenv()
FAST_TRACK_THRESHOLD = float(os.getenv("DAMAGE_THRESHOLD", "25000"))
```

---

### Q5: Can I add more sample documents?

**A:** Yes! Just add `.txt` or `.pdf` files to `sample_documents/`:

```bash
# Create new sample
cat > sample_documents/claim_sample_006.txt << 'EOF'
POLICY NUMBER: POL-2024-999999
NAME OF INSURED: Test Person
DATE OF LOSS: 02/08/2026
CLAIM TYPE: Auto Accident
ESTIMATE AMOUNT: $15,000
EOF

# Process it
python agent.py -i sample_documents/claim_sample_006.txt
```

**Best practices:**
- Use clear, consistent field names
- Include all mandatory fields
- Test with various claim types
- Document expected routing outcome

---

### Q6: How do I process a custom PDF file?

**A:** Just pass the path to the agent:

```bash
# Single PDF
python agent.py -i /path/to/your/claim.pdf

# Specific output location
python agent.py -i /path/to/claim.pdf -o /path/to/results.json
```

**Tips for best results:**
- Use standard form layouts (like ACORD forms)
- Ensure text is readable (not scanned)
- Use consistent field naming conventions
- Include all mandatory information

---

### Q7: What if fields aren't being extracted?

**A:** Check the field patterns in `src/field_extractor.py`:

```python
# Examine the patterns
FIELD_PATTERNS = {
    "policy_number": r"(?:POLICY\s*(?:NUMBER|#)|POLICY_NUMBER)[:\s]*([0-9A-Za-z-]+)",
    # The pattern should match your document's field names
}
```

**Debug a document:**
```python
from src.field_extractor import FieldExtractor

extractor = FieldExtractor()

# Read your document
with open("my_document.txt") as f:
    text = f.read()

# Test extraction
fields = extractor.extract_fields(text)

# Check what was found
for field, value in fields.items():
    if value:
        print(f"✓ {field}: {value}")
    else:
        print(f"✗ {field}: NOT FOUND")
```

**Add new patterns:**
```python
# In FIELD_PATTERNS dictionary
"my_new_field": r"CUSTOM_PATTERN_HERE"
```

---

### Q8: How do I disable fraud detection?

**A:** Modify `check_for_fraud_indicators()` in `src/field_extractor.py`:

```python
def check_for_fraud_indicators(self, text: str) -> List[str]:
    """Check for fraud-related keywords in document"""
    # Option 1: Return empty list (no fraud detected)
    return []
    
    # Option 2: Keep existing logic
    fraud_keywords = ["fraud", "inconsistent", "staged"]
    # ... rest
```

**Or comment out in routing:**
```python
# In determine_route() method
# fraud_indicators = self.extractor.check_for_fraud_indicators(document_text)
fraud_indicators = []  # Always empty
```

---

### Q9: Can I export results to other formats?

**A:** Currently JSON is built in. Add other formats:

```python
import csv
import xml.etree.ElementTree as ET

# Export to CSV
def export_to_csv(results, filename):
    import csv
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['policy_number', 'route', 'reasoning'])
        writer.writeheader()
        for r in results:
            fields = r['extractedFields']
            writer.writerow({
                'policy_number': fields.get('policy_number'),
                'route': r['recommendedRoute'],
                'reasoning': r['reasoning']
            })

# Export to CSV
export_to_csv(results, "output/claims.csv")
```

---

### Q10: How do I see detailed debug output?

**A:** Add logging to `agent.py`:

```python
import logging

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# In process_claim method, add:
def process_claim(self, document_path: str):
    logger.debug(f"Processing: {document_path}")
    
    document_text = self.parser.parse_document(document_path)
    logger.debug(f"Parsed {len(document_text)} characters")
    
    extracted_fields = self.extractor.extract_fields(document_text)
    logger.debug(f"Extracted {len(extracted_fields)} fields")
    
    # ... rest of code
```

**Run with debug output:**
```bash
python agent.py -i sample_documents 2>&1 | grep -i debug
```

---

## Performance Issues

### Problem: Slow PDF Processing

**Cause:** Large or complex PDF files

**Solutions:**

1. **Check file size:**
   ```bash
   ls -lh sample_documents/*.pdf
   # Large files (>50MB) will be slow
   ```

2. **Optimize PDF parsing:**
   ```python
   # In pdf_parser.py, add:
   def _parse_pdf(self, file_path: str) -> str:
       text = ""
       with pdfplumber.open(file_path) as pdf:
           # Process only first 10 pages for large files
           max_pages = min(10, len(pdf.pages))
           for page in pdf.pages[:max_pages]:
               text += page.extract_text() or ""
       return text
   ```

3. **Use batch processing:**
   ```bash
   # Process documents in parallel (future enhancement)
   python agent.py -i large_directory --parallel
   ```

---

## Data Quality Issues

### Problem: Fields extraction inconsistent

**Causes:**
- Non-standard document format
- Handwritten fields
- Font or encoding issues
- OCR artifacts

**Solutions:**

1. **Improve patterns for your documents:**
   ```python
   # Test and refine patterns
   import re
   
   pattern = r"YOUR_PATTERN_HERE"
   text = "your document text"
   match = re.search(pattern, text, re.IGNORECASE)
   print(match.group(1) if match else "No match")
   ```

2. **Use more flexible patterns:**
   ```python
   # Too strict
   r"POLICY NUMBER[:\s]*([0-9]{10})"
   
   # More flexible
   r"POLICY[:\s]*([0-9A-Za-z-]+)"
   ```

3. **Pre-process documents:**
   ```python
   # Clean text before extraction
   def clean_text(text):
       # Remove extra whitespace
       text = ' '.join(text.split())
       # Convert to uppercase for consistency
       text = text.upper()
       return text
   ```

---

## Integration Issues

### Problem: Can't import agent in another module

**Error:**
```
ModuleNotFoundError: No module named 'agent'
```

**Solution:**

```python
# In your file, add path to sys
import sys
from pathlib import Path

# Add agent directory to path
agent_dir = Path(__file__).parent.parent / "insurance-claims-agent"
sys.path.insert(0, str(agent_dir))

# Now you can import
from agent import ClaimsProcessingAgent
```

---

## Error Logs

### Common Error Messages

```
ERROR 1: "JSON decode error"
→ Output file corrupted, delete and rerun

ERROR 2: "UnicodeDecodeError"
→ File encoding issue, convert to UTF-8

ERROR 3: "Regex timeout"
→ Pattern too complex, simplify pattern

ERROR 4: "Memory error"
→ File too large, process in chunks
```

---

## Getting Help

### Check These Resources First

1. **For setup issues:** [01_project_setup.md](./01_project_setup.md)
2. **For library questions:** [02_libraries_and_dependencies.md](./02_libraries_and_dependencies.md)
3. **For algorithm details:** [03_algorithm_explanation.md](./03_algorithm_explanation.md)
4. **For examples:** [04_working_examples.md](./04_working_examples.md)

### Debug Tips

```bash
# 1. Check environment
python3 --version
pip --version
which python3

# 2. Verify dependencies
pip list | grep -E "pdfplumber|PyPDF2|python-dotenv"

# 3. Test imports
python3 -c "import pdfplumber, PyPDF2; print('✓ OK')"

# 4. Run single document
python agent.py -i sample_documents/claim_sample_001.txt

# 5. Check output
cat output/claims_processing_results.json | python3 -m json.tool | head -50
```

### Report Issues

When reporting errors, include:

1. **Python version:** `python3 --version`
2. **OS:** `uname -a`
3. **Error message:** Full traceback
4. **Sample document:** If possible
5. **Steps to reproduce:** Exact commands used

---

## Optimization Tips

### For Production Use

```python
# 1. Batch processing
agent = ClaimsProcessingAgent()
results = agent.process_multiple_claims("documents_dir")

# 2. Results caching
if cached_result_exists(document_id):
    return cached_result
else:
    result = process(document)
    cache_result(document_id, result)
    return result

# 3. Parallel processing (future)
from multiprocessing import Pool

with Pool(4) as p:
    results = p.map(process_claim, documents)
```

### Memory Optimization

```python
# Process large files in chunks
def process_large_directory(directory):
    batch_size = 50
    documents = list(Path(directory).glob("*.pdf"))
    
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        results = process_batch(batch)
        save_results(results)  # Don't keep all in memory
```

---

## Summary

**Most Common Issues & Quick Fixes:**

| Issue | Fix |
|-------|-----|
| Module not found | `source venv/bin/activate` |
| File not found | Check path with `ls` |
| Permission denied | `chmod 755 output` |
| No fields extracted | Check patterns in code |
| Wrong route | Verify thresholds/keywords |
| Slow processing | Check PDF size |

**Remember:** Check the specific guide file before this one for more details! 📚

---

**Still stuck?** Create a test case and debug step-by-step using the code examples above. You've got this! 💪
