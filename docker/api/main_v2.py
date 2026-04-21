import uuid
import json

from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import StreamingResponse
from redis import asyncio as aredis
from sqlalchemy import select

from connection_async import AsyncSessionFactory
from models import Conversation, Message


redis_client = aredis.from_url("redis://redis:6379", decode_responses=True)

app = FastAPI()


@app.post(
    "/conversations",
    summary="대화 시작 API",
)
async def create_conversation_handler():
    async with AsyncSessionFactory() as session:
        conversation = Conversation()
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
    return conversation

@app.get(
    "/conversations/{conversation_id}/messages",
    summary="전체 메세지 조회 API"
)
async def get_messages_handler(
    conversation_id: str
):
    async with AsyncSessionFactory() as session:
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.id.asc())
        )
        result = await session.execute(stmt)
        messages = result.scalars().all()
    return messages

@app.post(
    "/conversations/{conversation_id}/messages",
    summary="메세지 생성 API",
)
async def create_message_handler(
    conversation_id: str,
    user_input: str = Body(..., embed=True),
):
    async with AsyncSessionFactory() as session:
        # 1) 대화방 확인
        conversation = await session.get(Conversation, conversation_id)
        if not conversation:
            raise HTTPException(
                status_code=404, detail="Conversation Not Found"
            )
        
        # 2) 사용자 메시지 생성
        user_msg = Message(
            conversation_id=conversation.id,
            role="user",
            content=user_input,
        )
        session.add(user_msg)
        await session.flush()

        # 3) 이전 대화내역 조회
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.id.asc()) # id 기준 오름차순
        )
        result = await session.execute(stmt)
        messages = result.scalars().all()

        # Context Rot 방지
        # 1) message 개수가 N개 이상되면, 요약해서 저장
        # 2) 대화 내역 중에 주제가 바뀌면, 이전 메시지는 무시

        history = [
            {"role": m.role, "content": m.content} for m in messages
        ]
        
        # 4) 작업 내용을 Enqueue
        channel = conversation.id
        pubsub = redis_client.pubsub()
        await pubsub.subscribe(channel)

        task = {"channel": channel, "messages": history}
        await redis_client.lpush("queue", json.dumps(task))

        await session.commit()
    
    async def event_listener():
        assistant_text = ""

        async for message in pubsub.listen():
            if message["type"] != "message":
                continue
            
            token = message["data"]
            if token == "[DONE]":
                break

            assistant_text += token
            yield token

        # LLM 응답 메시지 저장
        async with AsyncSessionFactory() as session:
            assistant_msg = Message(
                conversation_id=conversation_id,
                role="assistant",
                content=assistant_text
            )
            session.add(assistant_msg)
            await session.commit()
        
        await pubsub.unsubscribe(channel)
        await pubsub.close()

    return StreamingResponse(
        event_listener(),
        media_type="text/event-stream",
    )
