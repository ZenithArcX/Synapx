# Project Setup Guide

## Overview

This guide walks you through setting up the Autonomous Insurance Claims Processing Agent on your system. The project follows modern Python best practices using virtual environments to keep your system clean and avoid dependency conflicts.

## Prerequisites

Before you start, ensure you have:

- **Python 3.8 or higher** - Check with: `python3 --version`
- **pip** (Python package manager) - Usually comes with Python
- **git** (optional, for version control) - Check with: `git --version`
- **Ubuntu 24.04+** or similar Linux distribution (Windows/Mac also compatible)
- **~500 MB disk space** for the project and dependencies

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.8 | 3.9 or higher |
| RAM | 512 MB | 2 GB+ |
| Disk Space | 500 MB | 1 GB+ |
| OS | Ubuntu/Linux | Ubuntu 24.04+ |

## Installation Steps (Ubuntu 24.04+)

### Step 1: Install venv Support (One-time)

On Ubuntu 24.04, Python is protected to keep the OS stable. Use `venv` for isolated environments:

```bash
sudo apt update
sudo apt install python3-venv python3-full -y
```

**What this does:**
- `python3-venv` - Allows you to create virtual environments
- `python3-full` - Complete Python installation (not just minimal)

### Step 2: Navigate to Project Directory

```bash
cd /mnt/data/projects/SYNAPX/insurance-claims-agent
```

Or wherever you've cloned/copied the project.

### Step 3: Create Virtual Environment

```bash
python3 -m venv venv
```

**What this does:**
- Creates a `venv/` folder with an isolated Python environment
- All dependencies will be installed here, not system-wide
- Keeps your system Python clean

**Why venv?**
- ✅ Prevents version conflicts
- ✅ Isolates this project from others
- ✅ Easy to delete (just remove the `venv/` folder)
- ✅ Professional best practice
- ✅ Required on Ubuntu 24.04+

### Step 4: Activate Virtual Environment

```bash
source venv/bin/activate
```

**Your prompt should now show `(venv)` prefix:**

```
(venv) user@machine:~/insurance-claims-agent$
```

**What this does:**
- Activates the isolated Python environment
- Commands like `pip` and `python` now use the virtual environment
- You're ready to install project dependencies

### Step 5: Upgrade pip

```bash
pip install --upgrade pip
```

**Why?**
- Ensures you have the latest pip version
- Better dependency resolution
- Faster package installation

### Step 6: Install Project Dependencies

```bash
pip install -r requirements.txt
```

**What this does:**
- Reads `requirements.txt` file
- Downloads and installs all required packages
- Installs them into your virtual environment (not system-wide)

**Expected output:**
```
Successfully installed pdfplumber-0.10.3 PyPDF2-3.0.1 python-dotenv-1.0.0
```

### Step 7: Verify Installation

```bash
python3 -c "import pdfplumber, PyPDF2; print('✓ All libraries installed correctly!')"
```

If successful, you'll see: `✓ All libraries installed correctly!`

## Project Structure After Setup

```
insurance-claims-agent/
├── venv/                          # Virtual environment (created in Step 3)
│   ├── bin/
│   │   ├── python                 # Python executable
│   │   ├── pip                    # Package manager
│   │   └── activate               # Activation script
│   ├── lib/                        # Installed packages
│   └── pyvenv.cfg
│
├── src/                            # Main source code
│   ├── __init__.py
│   ├── pdf_parser.py
│   ├── field_extractor.py
│   └── routing_engine.py
│
├── sample_documents/               # Test data
│   ├── claim_sample_001.txt
│   ├── claim_sample_002.txt
│   └── ...
│
├── output/                         # Results folder
│   └── claims_processing_results.json
│
├── agent.py                        # Main application
├── requirements.txt                # Dependencies list
└── README.md                       # Documentation
```

## Using the Virtual Environment

### Activating the Environment

Every time you work on this project, activate the virtual environment:

```bash
cd /mnt/data/projects/SYNAPX/insurance-claims-agent
source venv/bin/activate
```

### Deactivating the Environment

When you're done working:

```bash
deactivate
```

Your terminal prompt will return to normal (no `(venv)` prefix).

## Running the Application

Once the virtual environment is activated:

```bash
# Process all sample documents
python agent.py -i sample_documents

# Process a specific file
python agent.py -i sample_documents/claim_sample_001.txt

# Custom output location
python agent.py -i sample_documents -o my_results.json
```

## Common Setup Issues

### Issue: "ModuleNotFoundError: No module named 'pdfplumber'"

**Cause:** Virtual environment not activated

**Solution:**
```bash
source venv/bin/activate
```

### Issue: "command not found: python3"

**Cause:** Python not installed

**Solution:**
```bash
sudo apt install python3 python3-pip
```

### Issue: "Permission denied" when running setup script

**Cause:** Script not executable

**Solution:**
```bash
chmod +x setup.sh
./setup.sh
```

### Issue: "venv: command not found"

**Cause:** venv module not installed

**Solution:**
```bash
sudo apt install python3-venv
```

## Automated Setup

For convenience, use the provided setup script:

```bash
cd /mnt/data/projects/SYNAPX/insurance-claims-agent
chmod +x setup.sh
./setup.sh
```

This automatically performs all steps from 1-7.

## File Permissions on Linux

Make sure you have the correct permissions:

```bash
# Make scripts executable
chmod +x setup.sh
chmod +x agent.py

# Check permissions
ls -la agent.py setup.sh
```

## Environment Variables (Optional)

Create a `.env` file for configuration:

```bash
cat > .env << EOF
LOG_LEVEL=INFO
OUTPUT_FORMAT=JSON
DAMAGE_THRESHOLD=25000
EOF
```

Then load in your code (already supported in `agent.py`).

## Reinstalling Dependencies

If something goes wrong, reinstall:

```bash
# Deactivate first
deactivate

# Remove virtual environment
rm -rf venv

# Recreate and reinstall
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Upgrading Dependencies

To update all packages:

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## Summary Checklist

- [ ] Python 3.8+ installed
- [ ] venv module installed (`sudo apt install python3-venv`)
- [ ] Virtual environment created (`python3 -m venv venv`)
- [ ] Virtual environment activated (`source venv/bin/activate`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Installation verified (imported libraries successfully)
- [ ] Ready to run application

## Next Steps

Once setup is complete:

1. Read [02_libraries_and_dependencies.md](./02_libraries_and_dependencies.md) to understand what libraries are used
2. Read [03_algorithm_explanation.md](./03_algorithm_explanation.md) to learn how the agent works
3. Read [04_working_examples.md](./04_working_examples.md) to see real examples
4. Run the application: `python agent.py -i sample_documents`

## Troubleshooting

For more issues, see [05_troubleshooting_and_faq.md](./05_troubleshooting_and_faq.md).

---

**Setup Complete!** You're now ready to run the Insurance Claims Processing Agent. 🚀
