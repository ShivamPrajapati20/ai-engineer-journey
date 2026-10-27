import httpx, asyncio, time

URL = "https://httpbin.org/delay/1"

async def call(client: httpx.AsyncClient, i: int) -> int:
    response = await client.get(URL)
    return response.status_code

async def sequential() -> list[int]:
    results = []
    async with httpx.AsyncClient(timeout=30) as client:
        for i in range(10):
            results.append(await call(client,i))
    return results

async def concurrent() -> list[int]:
    async with httpx.AsyncClient(timeout=30) as client:
        return await asyncio.gather(*(call(client,i) for i in range(10)))

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(sequential())
    seq = time.perf_counter() - start
    print(f"Sequential: {seq:.2f} s")

    start = time.perf_counter()
    asyncio.run(concurrent())
    con = time.perf_counter() - start
    print(f"Concurrent: {con:.2f} s")

    print(f"Speedup: {seq/con:.1f}x")