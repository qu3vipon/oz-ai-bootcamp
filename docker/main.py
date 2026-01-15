import asyncio
import json
import uuid

from sqlalchemy import text
from fastapi import FastAPI, Depends, Body
from fastapi.responses import StreamingResponse
import redis.asyncio as redis

from connection import get_session

redis_client = redis.from_url("redis://redis:6379", decode_responses=True)


app = FastAPI()


@app.post("/generate")
async def generate(user_input: str = Body(...)):
    request_id = str(uuid.uuid4())
    channel = f"result:{request_id}"

    job = {
        "id": request_id,
        "input": user_input,
    }

    await redis_client.lpush("inference_queue", json.dumps(job))
    print("Job pushed to queue...")

    async def event_generator():
        pubsub = redis_client.pubsub()
        await pubsub.subscribe(channel)
        print("Start subscribe channel...")

        async for message in pubsub.listen():
            if message["type"] != "message":
                continue

            data = message["data"]

            if data == "[DONE]":
                break

            yield f"{data}"

        await pubsub.unsubscribe(channel)
        await pubsub.close()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
