# fetch_etl
Data Engineering Take Home: ETL off a SQS Queue

## Installation

### Initalize environment
```bash
git clone git@github.com:aschwa/fetch_etl.git
cd fetch_etl
conda env create  --file environment.yml
docker-compose build
docker-compose up
```
Wait for containers to run.

### Run App (in separate terminal)
```bash
conda activate fetch_env
cd app
uvicorn main:app
```

While app is running, you can visit http://127.0.0.1:8000 to run the app's functionality. 
1. Click the GET button
2. Click "Try it out"
3. Click Execute

### Check database 
```bash
 psql -d postgres -U postgres -p 5432 -h localhost -W
```
```sql
select * from user_logins;
```

## Design Questions

* How will you read messages from the queue?

Messages are read from the queue via `localstack_client` which allows a local client to run similarly to `boto3`. The messages are then loaded into dictionaries via `json.loads`, which can then be processed.
* What type of data structures should be used?

I created a `UserLogin` class based on `pydantic`'s  `BaseModel`. This would be useful down the road for additional processing and validation of the login events. 

* How will you mask the PII data so that duplicate values can be identified?

I use Fernet to encrypt the PII data. We can use a key that is stored securely to decrpyt the data, or just check that the encrypted value is unique to detect duplicates. I include the same Fernet key in settings in case we wanted to test the decryption.

* What will be your strategy for connecting and writing to Postgres?

I use `psycopg2` to connect and write to Postgres. With additional development time I would consider using `SQLAlchemy` to reflect the database schema in the `user_logins` table.
* Where and how will your application run?

I decided to create a FastAPI application to give the application a simple structure and a quick way to have a GUI via `Swagger UI`. FastAPI is run locally via Uvicorn. Again, this may have been overkill since we really only have one action/API route, but I wanted to make something that could theoretically be built-out with additional functionality.
