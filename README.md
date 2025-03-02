# Fastapi Example
* FastAPI
* Bearer Authentication
* SQLite database
* Alembic migrations
* ApiRouter

change JWT_SECRET_KEY in .env file with your own secret key

```shell
$ pip install -r requirements.txt
$ alembic upgrade head
$ fastapi run app/main.py --host localhost --port 8080
```

##
Testuser is:
```json
{
  "username": "testuser",
  "password": "test"
}
```
