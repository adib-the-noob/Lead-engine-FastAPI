# leadone-engine
Leadone-engine is the unified backend server of LeadOne, the brain-child of AA49.

## Installation
1. Make a virtual environment inside the engine folder by running `python3 -m venv env`
2. Activate the virtual environment by running `source env/bin/activate` (Linux) or `env\Scripts\activate` (Windows)
3. Install the requirements.txt file by running `pip install -r requirements.txt`
4. Create a Database in PostgreSQL named `leadengine-dev-db`
5. Run the server by running `uvicorn main:app --reload`

## API Documentation
The API documentation is available at `http://
localhost:8000/docs` or `http://localhost:8000/redoc` when the server is running.


## SQL admin
doc : https://aminalaee.dev/sqladmin/configurations/