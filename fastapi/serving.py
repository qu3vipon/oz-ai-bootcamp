import asyncio

from llama_cpp import Llama
from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse


# 모델 로드
llm = Llama(
    model_path="./models/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
    n_ctx=4096,
    n_threads=2,
    verbose=False,
    chat_format="llama-3",
)

# 시스템 프롬프트
SYSTEM_PROMPT = (
    "You are a concise assistant. "
    "Always reply in the same language as the user's input. "
    "Do not change the language. "
    "Do not mix languages."
)


app = FastAPI()

@app.post("/chats")
async def generate_chat_api(user_input: str = Body(...)):
    async def event_generator():
        response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ],
            max_tokens=256,
            temperature=0.6,  # 창의성/자유도(0 ~ 1)
            stream=True,
        )
        for chunk in response:
            token = chunk["choices"][0]["delta"].get("content")
            if token:
                yield token
                await asyncio.sleep(0)

    return StreamingResponse(
        event_generator(), media_type="text/event-stream"
    )
