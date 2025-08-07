# database-integration-with-fastapi-in-chatbot-system
database-integration-with-fastapi-in-chatbot-system

![DB-System](plots/DB-System.svg)


## USAGE

1. Clone the repo, using
```bash
git clone git@github.com:sulaiman-shamasna/database-integration-with-fastapi-in-chatbot-system.git
```
2. Assuming you have PostgreSQL database, create a database and call it ```ChatbotApplicationDatabase```.

3. In the project's directory, install the requirements, using
```bash
pip install -r requirements
```

4. Initiate alembic, using
```bash
alembic init alembic
```

5. create a ```.env``` file in the main directory, which should look like
```bash
DATABASE_URL=postgresql+asyncpg://postgres:**********@localhost/ChatbotApplicationDatabase
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ChatbotApplicationDatabase
DB_USER=postgres
DB_PASSWORD:**********

# Application Settings
APP_NAME=Chatbot Application
DEBUG=true 
```

6. In the main directory, run the application, using
```bash
uvicorn main:app --reload
```



