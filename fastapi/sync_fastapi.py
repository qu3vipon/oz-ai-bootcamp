import asyncio
import time

from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool


app = FastAPI()

@app.get("/sleep")
async def sleep_api():
    await run_in_threadpool(time.sleep, 5)
    return {"msg": "ok"}
