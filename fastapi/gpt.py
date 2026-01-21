from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse

from pydantic import BaseModel
from openai import AsyncOpenAI

from config import settings


client = AsyncOpenAI(api_key=settings.openai_api_key)

app = FastAPI()


class ResultSchema(BaseModel):
    result: str
    confidence: float

@app.post("/chat-gpt")
async def chat_gpt_api(user_input: str = Body(...)):
    async def event_generator():
        # OPEN AI 서버랑 연결 맺고, Streaming 데이터를 지속적으로 받음
        async with client.responses.stream(
            model="gpt-5-mini",
            input=user_input,
            text_format=ResultSchema
        ) as stream:
            async for event in stream:
                if event.type == "response.output_text.delta":
                    yield event.delta
                elif event.type == "response.completed":
                    break
    return StreamingResponse(event_generator(), media_type="text/event-stream")
