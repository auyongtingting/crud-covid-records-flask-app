# crud-covid-records-flask-app 
A simple application to explore around postgreSQL alongside CRUD functions. 

## How to run locally

1. Preparation of PostgreSQL database
Create a database with a preferred name 

2. Preparation of .env file 
Ensure that you have created .env file with the following variable declared

```
DEV_DB='postgresql://<username>:<password>@<hostname>:<port>/<database_name>'
```

e.g., DEV_DB='postgresql://auyongtingting:thisismypassword@localhost:5432/database-example'

3. Create tables in database 

```
python
from app import db
db.create_all()
```

4. Run the application 

```
python app.py
```

Happy running!

