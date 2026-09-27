.PHONY: install run clean

# Setup virtual environment and install dependencies
install:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

# Run the Streamlit AI Harness
run:
	./venv/bin/streamlit run app.py

# Clean up caches and virtual environment
clean:
	rm -rf venv
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
