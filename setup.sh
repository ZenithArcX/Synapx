#!/bin/bash
# Setup script for Insurance Claims Processing Agent
# Professional virtual environment setup for Ubuntu 24.04+

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Insurance Claims Processing Agent - Setup Script          ║"
echo "║  Ubuntu 24.04+ Professional Environment Configuration      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Check if venv is installed
echo "📦 Step 1: Checking Python venv support..."
if python3 -m venv --help > /dev/null 2>&1; then
    echo "✅ venv is available"
else
    echo "⚠️  venv not found. Installing Python venv support..."
    sudo apt install python3-venv python3-full -y
    echo "✅ venv installed"
fi
echo ""

# Step 2: Create virtual environment
echo "🔧 Step 2: Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⏭️  Virtual environment already exists (venv/)"
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Step 3: Activate virtual environment
echo "🚀 Step 3: Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated - (venv) prefix should appear above"
echo ""

# Step 4: Upgrade pip
echo "⬆️  Step 4: Upgrading pip..."
pip install --quiet --upgrade pip
echo "✅ pip upgraded"
echo ""

# Step 5: Install requirements
echo "📚 Step 5: Installing dependencies from requirements.txt..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Step 6: Verify installation
echo "✔️  Step 6: Verifying installation..."
python3 -c "import pdfplumber; print('✅ pdfplumber available')"
python3 -c "import PyPDF2; print('✅ PyPDF2 available')"
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ Setup Complete!                                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Activate environment: source venv/bin/activate"
echo "  2. Run agent: python agent.py -i sample_documents"
echo "  3. Check results: cat output/claims_processing_results.json"
echo ""
echo "To deactivate later: deactivate"
echo ""
