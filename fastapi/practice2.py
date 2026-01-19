import asyncio


async def a():
    await asyncio.sleep(0.1)
    print("A 시작") 
    await asyncio.sleep(0.0)
    print("A 끝")

async def b():
    await asyncio.sleep(0.2)
    print("B 시작")  
    await asyncio.sleep(0.2)
    print("B 끝")

async def c():
    await asyncio.sleep(0.0)
    print("C 시작") 
    await asyncio.sleep(0.3)
    print("C 끝")

async def main():
    await asyncio.gather(a(), b(), c())

asyncio.run(main())
# 실행 중(한 번에 1개씩), 대기 중(I/O 작업 중), 준비 중(I/O 작업 완료)
