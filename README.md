# Test App For Schemathesis 

1. Quick start run: ./setup.sh 
2. Rebuild run: ./setup.sh rebuild 
3. Clean run ./setup.sh clean  ***warning this deletes all ophan contianers and volumeson your machine*** 


# Testing 

cd /backend 
# create virtual environment using uv 
uv venv
# Install requirements 
uv pip install -r requirements.txt
# Run the schemathesis coverage tests 
uv run pytest -v

# Run shemathesis Full tests

schemathesis run http://localhost:8000/openapi.json
