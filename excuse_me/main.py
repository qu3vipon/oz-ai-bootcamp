import asyncio
import json

import numpy as np

from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from sqlalchemy import select

from connection import engine, AsyncSessionFactory
from config import settings
from models import Base, Profile


client = AsyncOpenAI(api_key=settings.openai_api_key)

@asynccontextmanager
async def lifespan(_):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)


class GenerateIn(BaseModel):
    situation: str = Field(..., min_length=1, max_length=1000)
    tone: str = Field("light_humor", description="neutral|light_humor|humor|strong_humor|dark_humor")


class GenerateOut(BaseModel):
    excuse: str
    used_profile: list[str]
    tone: str


def cosine(a: list[float], b: list[float]) -> float:
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-12
    return float(np.dot(a, b) / denom)


async def embed(text: str) -> list[float]:
    r = await client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return r.data[0].embedding


@app.post("/profile")
async def upload_profile(file: UploadFile = File(...)):
    raw = (await file.read()).decode("utf-8", errors="ignore")
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]

    async with AsyncSessionFactory() as session:
        # 기존 문장들 가져오기
        result = await session.execute(select(Profile.content))
        existing = set(result.scalars().all())

        # 새 문장만 필터
        new_lines = [ln for ln in lines if ln not in existing]

        if not new_lines:
            return {"stored_lines": 0, "message": "No new lines"}

        # 새 문장만 임베딩
        embeddings = await asyncio.gather(*(embed(ln) for ln in new_lines))

        # 저장
        for ln, e in zip(new_lines, embeddings):
            session.add(Profile(content=ln, embedding=json.dumps(e)))

        await session.commit()

    return {"stored_lines": len(new_lines)}


tone_rule = {
    "neutral": "유머 없이 담백하고 사실 위주로.",
    "light_humor": "가벼운 위트 1회 정도, 무난하게.",
    "humor": "자연스러운 농담 몇 번, 친근하게.",
    "strong_humor": "꽤 웃기게, 과장과 드립 허용.",
    "dark_humor": "블랙코미디 스타일. 센 농담 허용하되 혐오·차별·폭력·실명 모욕은 금지.",
}

@app.post("/generate", response_model=GenerateOut)
async def generate(body: GenerateIn):
    # 내 프로필 정보 조회
    async with AsyncSessionFactory() as session:
        rows = (await session.execute(select(Profile))).scalars().all()

    # 입력된 상황(body.situation)을 임베딩 벡터로 변환
    q = await embed(body.situation)

    scored = []
    for r in rows:
        e = json.loads(r.embedding)

        # 입력 임베딩(q)과 각 프로필 임베딩(e)의 코사인 유사도 계산
        scored.append((cosine(q, e), r.content))

    # 유사도 기준으로 내림차순 정렬 (가장 유사한 게 앞에 오도록)
    scored.sort(reverse=True)

    # 상위 3개 프로필의 content만 추출
    used = [t for _, t in scored[:3]]

    # tone 값에 따라 말투 규칙 선택, 없으면 기본값 사용
    tone = tone_rule.get(body.tone, "유머 없이 담백하고 사실 위주로.")

    prompt = f"""
[나에 대한 정보]
- """ + "\n- ".join(used) + f"""

[상황]
{body.situation}

[작성 규칙]
- 위 '나에 대한 정보'에 어긋나지 않게, 내가 실제로 보낼 법한 변명/상황 설명 메시지를 한국어로 작성.
- 새로운 사실(구체 시간/장소/사건)은 만들어내지 말고, 모르면 안전하게 완곡하게.
- {tone}

[출력]
메시지 본문만 출력.
""".strip()

    resp = await client.responses.create(model="gpt-5-mini", input=prompt)
    return GenerateOut(excuse=resp.output_text.strip(), used_profile=used, tone=tone)
