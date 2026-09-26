#!/bin/bash
echo "🚀 Launching Autonomous AI Harness..."

# Ensure we are in the project directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Check if venv exists, if not, something went wrong with setup
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please ensure dependencies are installed."
    exit 1
fi

# Activate virtual environment and run streamlit
source venv/bin/activate
streamlit run app.py --server.port 8501
