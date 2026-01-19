import asyncio
import time


async def async_sleep():
    await asyncio.sleep(3)

async def blocking_sleep():
    time.sleep(3)

async def main():
    coro1 = blocking_sleep()
    coro2 = async_sleep()
    await asyncio.gather(coro1, coro2) # 이벤트 루프한테 코루틴들 넘기는 함수

asyncio.run(main())