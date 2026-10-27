import asyncio, time
import httpx

BASE = "http://127.0.0.1:8000"

async def hit(path: str, n: int = 5) -> None:
    async with httpx.AsyncClient(timeout=60) as client:
        start = time.perf_counter()
        await asyncio.gather(*(client.get(BASE + path) for _ in range(n)))
        print(f"{path:12} {n} requests at once: {time.perf_counter() - start:.2f} s")


async def health_during_bad() -> None:
    async with httpx.AsyncClient(timeout=60) as client:
        bad = asyncio.gather(*(client.get(BASE + "/bad") for _ in range(5)))
        await asyncio.sleep(0.1)                     # let /bad start first
        start = time.perf_counter()
        await client.get(BASE + "/health")
        print(f"/health while /bad runs: {time.perf_counter() - start:.2f} s")
        await bad


async def main() -> None:
    for path in ["/good-async", "/good-sync", "/bad"]:
        await hit(path)
    await health_during_bad()


if __name__ == "__main__":
    asyncio.run(main())