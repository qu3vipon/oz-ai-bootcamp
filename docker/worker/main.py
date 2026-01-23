import json
import redis

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

def inference_and_publish(channel, user_input):
    print("추론 시작...")
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
        max_tokens=256,
        temperature=0.7,
        stream=True,
    )

    for chunk in response:
        token = chunk["choices"][0]["delta"].get("content")
        if token:
            redis_client.publish(channel, token)
    
    redis_client.publish(channel, "[DONE]")
    print("추론 종료...")


def run():
    while True:
        # Queue를 확인해서, Job(job_id, input) 꺼내기
        _, job_data = redis_client.brpop("inference_queue")
        
        job = json.loads(job_data)

        job_id = job["id"]
        user_input = job["input"]

        channel = f"result:{job_id}"

        # 추론 & publish
        try:
            inference_and_publish(channel=channel, user_input=user_input)
        except Exception as e:
            print(f"[Error] {str(e)}")
            redis_client.publish(channel, "[DONE]")


# 이 파일을 직접한 실행한 경우에만, run() 호출
if __name__ == "__main__":
    run()
