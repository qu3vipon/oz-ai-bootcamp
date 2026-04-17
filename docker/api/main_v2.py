import uuid

from sqlalchemy import select
from fastapi import Body


@app.post("/chats")
async def generate_chat_handler(
    user_input: str = Body(..., embed=True),
    conversation_id: str | None = Body(None),
):
    async with SessionFactory() as session:
        # 1. conversation 생성 or 조회
        if not conversation_id:
            conversation = Conversation()
            session.add(conversation)
            await session.flush()  # id 확보
        else:
            conversation = await session.get(Conversation, conversation_id)
            if not conversation:
                raise Exception("conversation not found")

        # 2. user 메시지 저장
        user_msg = Message(
            conversation_id=conversation.id,
            role="user",
            content=user_input,
        )
        session.add(user_msg)

        # 3. history 조회
        result = await session.execute(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.id.asc())
        )
        messages = result.scalars().all()

        history = [{"role": m.role, "content": m.content} for m in messages]

        # 4. worker로 전달
        pubsub = redis_client.pubsub()
        await pubsub.subscribe(conversation.id)

        task = {
            "conversation_id": conversation.id,
            "messages": history,
        }
        await redis_client.lpush("queue", json.dumps(task))

        await session.commit()

    async def event_generator():
        assistant_text = ""

        async for message in pubsub.listen():
            if message["type"] != "message":
                continue

            token = message["data"]

            if token == "[DONE]":
                break

            assistant_text += token
            yield token

        # 응답 저장
        async with SessionFactory() as session:
            session.add(
                Message(
                    conversation_id=conversation.id,
                    role="assistant",
                    content=assistant_text,
                )
            )
            await session.commit()

        await pubsub.unsubscribe(channel)
        await pubsub.close()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )
