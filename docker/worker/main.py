import json
import redis
from llama_cpp import Llama


redis_client = redis.from_url(
    "redis://redis:6379", 
    decode_responses=True,
    socket_timeout=None,
)

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


def run():
    while True:
        # 1) Queue에서 task를 dequeue
        _, task = redis_client.brpop("queue")

        task_data: dict = json.loads(task)

        # 2) (반복) 추론 -> 토큰 -> Publish
        response_generator = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": task_data["user_input"]},
            ],
            max_tokens=256,
            temperature=0.7,
            stream=True,
        )

        channel = task_data["channel"]
        for chunk in response_generator:
            token = chunk["choices"][0]["delta"].get("content")
            if token:
                redis_client.publish(channel, token)

        # 3) 추론 종료 알림: [Done] 메시지 전송
        redis_client.publish(channel, "[DONE]")


# 이 파일이 직접 실행한 경우에만, run() 호출
if __name__ == "__main__":
    run()
