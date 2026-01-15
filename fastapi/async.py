import asyncio
import time


async def a():
    print("A 시작") # 1
    await asyncio.sleep(4) # 2
    print("A 종료") # 6

async def b():
    print("B 시작") # 3
    await asyncio.sleep(2) # 4
    print("B 종료") # 5

async def main():
    start = time.time()
    await asyncio.gather(a(), b())
    end = time.time()
    print(f"{end - start:.3f}초")

asyncio.run(main())
