# User Guide - Complete Documentation

Welcome to the comprehensive user guide for the Insurance Claims Processing Agent! This folder contains everything you need to understand, set up, and use the system.

## 📚 Guide Structure

### 1. [Project Setup](./01_project_setup.md) ⚙️

**What you'll learn:**
- How to install Python and dependencies
- Creating and activating virtual environments
- Step-by-step setup instructions
- Troubleshooting common setup issues
- Project structure overview

**Best for:** First-time users, installation help

**Time:** 15-20 minutes to complete

**Prerequisites:** None, just have Python 3.8+

---

### 2. [Libraries & Dependencies](./02_libraries_and_dependencies.md) 📦

**What you'll learn:**
- Every library used and why
- How each library is used in the code
- Import statements and their purposes
- Standard library modules explained
- Performance impact of dependencies
- Security and version management

**Best for:** Understanding what makes the project work

**Time:** 10-15 minutes to read

**Prerequisites:** Completed Setup guide

**Key Topics:**
- `pdfplumber` - PDF text extraction
- `PyPDF2` - PDF manipulation
- `python-dotenv` - Configuration management
- Python standard library modules

---

### 3. [Algorithm Explanation](./03_algorithm_explanation.md) 🧠

**What you'll learn:**
- How the 4-stage pipeline works
- Detailed explanations of each processing stage
- Regex pattern matching for field extraction
- Validation algorithms
- Intelligent routing decision tree
- Performance metrics and time complexity

**Best for:** Understanding the technical approach

**Time:** 20-30 minutes to read

**Prerequisites:** Basic Python knowledge helpful

**Key Sections:**
1. Document Parsing - Converting files to text
2. Field Extraction - Using regex patterns
3. Field Validation - Checking completeness
4. Intelligent Routing - Making decisions

---

### 4. [Working Examples](./04_working_examples.md) 🎯

**What you'll learn:**
- Real examples showing each routing scenario
- Step-by-step processing walkthroughs
- Input documents and expected outputs
- JSON results interpretation
- Batch processing examples
- Programmatic usage examples

**Best for:** Seeing the system in action

**Time:** 15-20 minutes to read

**Prerequisites:** None, but Algorithm guide helpful

**5 Complete Examples:**
1. Standard Collision Claim → FAST_TRACK
2. High-Value Claim → STANDARD_REVIEW
3. Fraud Investigation Flag → INVESTIGATION_FLAG
4. Injury Claim → SPECIALIST_QUEUE
5. Incomplete Claim → MANUAL_REVIEW

---

### 5. [Troubleshooting & FAQ](./05_troubleshooting_and_faq.md) 🆘

**What you'll learn:**
- Common problems and solutions
- Frequently asked questions
- Debug techniques
- Performance optimization
- Data quality improvement
- Error message explanations

**Best for:** Solving problems and customization

**Time:** As needed

**Prerequisites:** Have encountered an issue

**Covers:**
- Module import errors
- File and permission issues
- PDF extraction problems
- Customization (thresholds, keywords)
- Performance troubleshooting
- Data quality issues

---

### 6. [Frontend and API Integration](./06_frontend_and_api_integration.md)

**What you'll learn:**
- How the React UI connects to the Python API
- API endpoints and request flow
- How the API links to the Python modules
- Running the UI locally

**Best for:** Simple UI integration and demo setup

**Time:** 10-15 minutes to read

**Prerequisites:** Setup completed

**Key Topics:**
- React UI upload flow
- Flask API routing
- Module linkage to agent pipeline

---

## 🚀 Quick Start Path

### For Beginners

1. **Start here:** [Project Setup](./01_project_setup.md)
   - Get the system running
   - Create virtual environment
   - Install dependencies

2. **Then read:** [Working Examples](./04_working_examples.md)
   - See actual results
   - Understand different scenarios
   - Run first command

3. **When curious:** [Libraries & Dependencies](./02_libraries_and_dependencies.md)
   - Learn what makes it work
   - Understand the tools used

4. **For deep dive:** [Algorithm Explanation](./03_algorithm_explanation.md)
   - Understand the logic
   - Learn technical details

5. **If stuck:** [Troubleshooting & FAQ](./05_troubleshooting_and_faq.md)
   - Find solutions
   - Get unstuck

### For Developers

1. Start with [Algorithm Explanation](./03_algorithm_explanation.md)
2. Then [Libraries & Dependencies](./02_libraries_and_dependencies.md)
3. Reference [Working Examples](./04_working_examples.md)
4. Use [Troubleshooting & FAQ](./05_troubleshooting_and_faq.md) as needed
5. Add UI with [Frontend and API Integration](./06_frontend_and_api_integration.md)

### For Ops/DevOps

1. [Project Setup](./01_project_setup.md) - understanding deployment
2. [Troubleshooting & FAQ](./05_troubleshooting_and_faq.md) - performance & optimization
3. [Libraries & Dependencies](./02_libraries_and_dependencies.md) - version management

---

## 📖 How to Use These Guides

### Reading the Guides

Each guide is standalone but they reference each other:

```
Setup → Libraries → Algorithm → Examples → Troubleshooting
```

However, you can jump to any section based on your needs.

### Code Examples

All guides include code snippets you can copy and run:

```python
# Most code is marked with context showing where it appears
# Example from src/pdf_parser.py:
def parse_document(self, file_path: str):
    # ... implementation
```

### Tables & Diagrams

Complex topics use tables and ASCII diagrams for clarity:

```
┌─────────────────────┐
│  4-Stage Pipeline   │
│  Parse → Extract    │
│  Validate → Route   │
└─────────────────────┘
```

### Terminal Commands

Commands you can actually run are highlighted:

```bash
# Executable commands appear in gray boxes
python agent.py -i sample_documents
```

---

## 🎯 Common Learning Goals

### "I want to run the agent"
→ Read: [Project Setup](./01_project_setup.md) + [Working Examples](./04_working_examples.md)

### "I want to understand the code"
→ Read: [Algorithm Explanation](./03_algorithm_explanation.md) + [Libraries & Dependencies](./02_libraries_and_dependencies.md)

### "I want to customize it"
→ Read: [Troubleshooting & FAQ](./05_troubleshooting_and_faq.md) - Customization section

### "I want to fix a problem"
→ Read: [Troubleshooting & FAQ](./05_troubleshooting_and_faq.md) - Problem matching

### "I want to deploy it"
→ Read: [Project Setup](./01_project_setup.md) + [Troubleshooting & FAQ](./05_troubleshooting_and_faq.md)

### "I want to integrate it"
→ Read: [Working Examples](./04_working_examples.md) - Programmatic Usage section

---

## 📊 Quick Reference

### File Overview

| File | Lines | Focus | Read Time |
|------|-------|-------|-----------|
| [01_project_setup.md](./01_project_setup.md) | ~400 | Installation | 15 min |
| [02_libraries_and_dependencies.md](./02_libraries_and_dependencies.md) | ~500 | Libraries | 15 min |
| [03_algorithm_explanation.md](./03_algorithm_explanation.md) | ~600 | How it works | 25 min |
| [04_working_examples.md](./04_working_examples.md) | ~700 | Real examples | 20 min |
| [05_troubleshooting_and_faq.md](./05_troubleshooting_and_faq.md) | ~550 | Problems & fixes | As needed |
| [06_frontend_and_api_integration.md](./06_frontend_and_api_integration.md) | ~250 | UI + API | 10 min |

### Key Concepts by Guide

| Concept | Guide | Section |
|---------|-------|---------|
| Virtual Environment | Setup | Step 3-4 |
| pdfplumber | Libraries | Section 1 |
| Regex Patterns | Algorithm | Stage 2 |
| Validation | Algorithm | Stage 3 |
| Routing Tree | Algorithm | Stage 4 |
| Field Extraction | Examples | Each example |
| Error Handling | Troubleshooting | All sections |

---

## 💾 File Locations

All guide files are in `/user_guide/`:

```
user_guide/
├── README.md (this file)
├── 01_project_setup.md
├── 02_libraries_and_dependencies.md
├── 03_algorithm_explanation.md
├── 04_working_examples.md
└── 05_troubleshooting_and_faq.md
└── 06_frontend_and_api_integration.md
```

Access from the project root:

```bash
cd /mnt/data/projects/SYNAPX/insurance-claims-agent
ls user_guide/
cat user_guide/01_project_setup.md
```

---

## 🔗 Cross-References

### From [Project Setup](./01_project_setup.md)
- References [Libraries](./02_libraries_and_dependencies.md) for dependency details
- Links to [Troubleshooting](./05_troubleshooting_and_faq.md) for setup issues

### From [Libraries & Dependencies](./02_libraries_and_dependencies.md)
- References [Algorithm](./03_algorithm_explanation.md) for how libraries are used
- References [Examples](./04_working_examples.md) for practical usage

### From [Algorithm Explanation](./03_algorithm_explanation.md)
- References [Examples](./04_working_examples.md) for real demonstrations
- Links to [Troubleshooting](./05_troubleshooting_and_faq.md) for performance issues

### From [Working Examples](./04_working_examples.md)
- References [Algorithm](./03_algorithm_explanation.md) for implementation details
- Links to [Troubleshooting](./05_troubleshooting_and_faq.md) for debugging

### From [Troubleshooting & FAQ](./05_troubleshooting_and_faq.md)
- References all other guides for detailed information
- Provides quick links to relevant sections

---

## 🎓 Learning Path

### Beginner Path (1 hour)
1. Project Setup (20 min)
2. Working Examples (20 min)
3. Troubleshooting FAQ - If needed (20 min)

### Intermediate Path (1.5 hours)
1. Project Setup (20 min)
2. Libraries & Dependencies (15 min)
3. Working Examples (20 min)
4. Troubleshooting FAQ (15 min)

### Advanced Path (2 hours)
1. Algorithm Explanation (30 min)
2. Libraries & Dependencies (20 min)
3. Working Examples (20 min)
4. Troubleshooting FAQ (20 min)
5. Code study (30 min)

### Expert Path (3+ hours)
Read all guides in order:
1. Project Setup
2. Libraries & Dependencies
3. Algorithm Explanation
4. Working Examples
5. Troubleshooting & FAQ
6. Study source code: `src/*.py`

---

## ❓ Frequently Asked Questions

**Q: Where should I start?**
A: [Project Setup](./01_project_setup.md) if you haven't installed yet, else [Working Examples](./04_working_examples.md)

**Q: How do I understand the code?**
A: Read [Algorithm Explanation](./03_algorithm_explanation.md) then [Libraries & Dependencies](./02_libraries_and_dependencies.md)

**Q: How do I troubleshoot an error?**
A: Go to [Troubleshooting & FAQ](./05_troubleshooting_and_faq.md) and search for your error

**Q: Can I modify the system?**
A: Yes! See [Troubleshooting & FAQ](./05_troubleshooting_and_faq.md) - Customization questions

**Q: How do I integrate this into my app?**
A: See [Working Examples](./04_working_examples.md) - Programmatic Usage section

**Q: How do I deploy this?**
A: See [Project Setup](./01_project_setup.md) - Setup Steps, then virtual environment section

---

## 📞 Getting Help

When you get stuck:

1. **Check Troubleshooting** → [05_troubleshooting_and_faq.md](./05_troubleshooting_and_faq.md)
2. **Reference Examples** → [04_working_examples.md](./04_working_examples.md)
3. **Review Algorithm** → [03_algorithm_explanation.md](./03_algorithm_explanation.md)
4. **Check Dependencies** → [02_libraries_and_dependencies.md](./02_libraries_and_dependencies.md)
5. **Verify Setup** → [01_project_setup.md](./01_project_setup.md)

---

## 🎉 You're Ready!

Pick a guide and start learning. Everything is documented for you!

**Recommended first steps:**
```bash
# 1. Read setup
cat user_guide/01_project_setup.md | head -50

# 2. Follow setup
source venv/bin/activate
pip install -r requirements.txt

# 3. Run examples
python agent.py -i sample_documents

# 4. Read examples guide
cat user_guide/04_working_examples.md

# 5. Explore algorithm
cat user_guide/03_algorithm_explanation.md
```

---

**Version:** 1.0
**Date:** February 2026
**Status:** Complete & Ready to Use ✅
