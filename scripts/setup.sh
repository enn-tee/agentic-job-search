#!/bin/bash
# Setup script for the Agentic Resume Tailoring System

set -e

echo "🎯 Agentic Resume Tailoring System - Setup"
echo "==========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your ANTHROPIC_API_KEY"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

# Run setup tests
echo "Running setup verification tests..."
pytest tests/test_setup.py -v
echo ""

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your ANTHROPIC_API_KEY"
echo "2. Review the QUICKSTART.md guide"
echo "3. Try the example:"
echo ""
echo "   python main.py tailor \\"
echo "     --job-text examples/sample_job_posting.txt \\"
echo "     --company 'MedTech Solutions' \\"
echo "     --title 'Senior Healthcare Data Analyst' \\"
echo "     --industry healthcare"
echo ""
echo "Happy job hunting! 🚀"
