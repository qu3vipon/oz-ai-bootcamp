import asyncio
import time

# 1) await는 항상 async 안에서만 쓸 수 있다
async def hello():
    await asyncio.sleep(1)
    print("hello")

# 2) await는 기다려야 하는 작업(awaitable)에 대해서만 쓸 수 있다
#   -> await 뒤에는 "코루틴 친구들"만 올 수 있다
async def hello2():
    # time.sleep(), print() -> 코루틴 친구들 X
    await asyncio.sleep(1)

asyncio.run(hello2())
