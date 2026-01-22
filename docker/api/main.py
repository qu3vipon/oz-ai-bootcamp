from fastapi import FastAPI
from sqlalchemy import text

from connection import SessionFactory


app = FastAPI()

@app.get("/health")
def health_check_api():
    with SessionFactory() as session:
        stmt = text("SELECT name FROM test LIMIT 1")
        result = session.execute(stmt).fetchone()
    return {"ping": "pong"}
