# Test App For Schemathesis 

1. Quick start run: ./setup.sh 
2. Rebuild run: ./setup.sh rebuild 
3. Clean run ./setup.sh clean  ***warning this deletes all ophan contianers and volumeson your machine*** 


# If pgbouncer image fails to build. 

1. Download the pgbouncer binaries from : https://www.pgbouncer.org/downloads/files/1.25.0/pgbouncer-1.25.0.tar.gz

2. Copy the Docker file and docker-entrypoint.sh from the current current pgbouncer folder and to another location. 

3. Delete original pgboucer folder and replace with newly downloaded binary in the repo. 

4. Copy the Docker file and the docker-entrypoint.sh to the new folder and run ./setup.sh up 


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
