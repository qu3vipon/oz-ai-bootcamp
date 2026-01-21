from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health_check_api():
    return {"ping": "pong"}
