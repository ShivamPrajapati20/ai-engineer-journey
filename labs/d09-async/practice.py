import asyncio
import time

async def fake_call(i: int) -> str:
    await asyncio.sleep(1)
    return f"result {i}"

# print(asyncio.run(fake_call(1)))


async def sequencial() -> list[str]:
    results = []
    for i in range(10):
        results.append(await fake_call(i))
    return results

start = time.perf_counter()
asyncio.run(sequencial())
print(f"Sequencial: ", round(time.perf_counter() - start, 2),"s")

async def concurrent() -> list[str]:
    return await asyncio.gather(*(fake_call(i) for i in range(10)))


start = time.perf_counter()
results = asyncio.run(concurrent())
print(f"Concurrent: ", round(time.perf_counter() - start, 2),"s")
print(results[:3])

async def bad_call(i: int) -> int:
    time.sleep(1)
    return i

async def run_bad() -> list[int]:
    return await asyncio.gather(*(bad_call(i) for i in range(10)))

start = time.perf_counter()
asyncio.run(run_bad())
print(f"Blocking inside async: ", round(time.perf_counter() - start, 2),"s")