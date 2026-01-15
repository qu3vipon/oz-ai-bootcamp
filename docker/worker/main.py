import asyncio
import json
import redis.asyncio as redis
from llama_cpp import Llama

redis_client = redis.from_url("redis://redis:6379", decode_responses=True)

llm = Llama(
    model_path="./models/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
    n_ctx=4096,
    n_threads=2,
    verbose=False,
    chat_format="llama-3",
)

SYSTEM_PROMPT = (
    "You are a concise assistant. "
    "Always reply in the same language as the user's input. "
    "Do not change the language. "
    "Do not mix languages."
)

async def run_inference_and_publish(channel: str, user_input: str):
    print("Start inference job...")
    resp = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
        max_tokens=256,
        temperature=0.7,
        stream=True
    )

    for chunk in resp:
        token = chunk["choices"][0]["delta"].get("content")
        if token:
            # 토큰을 Redis Pub/Sub으로 전송
            await redis_client.publish(channel, token)
            await asyncio.sleep(0)  # 이벤트 루프 양보

    # 작업 완료 신호
    await redis_client.publish(channel, "[DONE]")
    print("End inference job...")


async def process_jobs():
    while True:
        # Queue에서 작업 하나 꺼내기
        _, job_data = await redis_client.brpop("inference_queue")
        print("New job dequeued...")

        job = json.loads(job_data)
        request_id = job["id"]
        user_input = job["input"]

        channel = f"result:{request_id}"

        try:
            await run_inference_and_publish(channel, user_input)
        except Exception as e:
            await redis_client.publish(channel, f"[ERROR] {str(e)}")
        finally:
            await redis_client.publish(channel, "[DONE]")

if __name__ == "__main__":
    asyncio.run(process_jobs())
