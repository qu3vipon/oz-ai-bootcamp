import json
import uuid

from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from redis import asyncio as aredis


redis_client = aredis.from_url("redis://redis:6379", decode_responses=True)

app = FastAPI()

@app.post("/generate")
async def generate_api(user_input: str = Body(...)):
    # job_id 생성
    job_id = str(uuid.uuid4())
    
    # 결과 채널 구독
    channel = f"result:{job_id}"

    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel)
    print(f"구독 시작: {job_id}")

    # Enqueue(LPUSH)
    job = {"id": job_id, "input": user_input}
    await redis_client.lpush("inference_queue", json.dumps(job))
    print(f"큐에 작업 추가: {job}")

    # 결과를 돌려받아서 응답
    async def event_generator():
        print("Listening 시작...")
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue

            data = message["data"]
            if data == "[DONE]":
                break
            yield data
        
        await pubsub.unsubscribe(channel)
        await pubsub.close()
        print("Listening 종료...")

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
