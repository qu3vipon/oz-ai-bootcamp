import asyncio

from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from llama_cpp import Llama

app = FastAPI()

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

from openai import AsyncOpenAI

@app.post("/generate")
async def generate(user_input: str = Body(...)):
    async def event_generator():
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
                yield token
                await asyncio.sleep(0)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
from config import settings

client = AsyncOpenAI(api_key=settings.openai_api_key)



@app.post("/chat-gpt")
async def call_chat_gpt(user_input: str = Body(...)):
    async def event_generator():
        async with client.responses.stream(
            model="gpt-4.1-mini",
            input=user_input
        ) as stream:
            async for event in stream:
                if event.type == "response.output_text.delta":
                    yield event.delta
                elif event.type == "response.completed":
                    break

    return StreamingResponse(event_generator(), media_type="text/plain")
