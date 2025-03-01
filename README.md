# Fastapi Example
* FastAPI
* Bearer Authentication
* SQLite database
* Alembic migrations
* ApiRouter

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
  "password": "testpassword"
}
```