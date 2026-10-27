import asyncio, time
from fastapi import FastAPI

app = FastAPI()

@app.get("/good-async")
async def good_async() -> dict[str, str]:
    await asyncio.sleep(1)
    return {"type":"async def + await"}

@app.get("/good-sync")
def good_sync() -> dict[str, str]:
    time.sleep(1)
    return {"type":"def + blocking call"}

@app.get("/bad")
async def bad() -> dict[str,str]:
    time.sleep(1)
    return {"type":"async def + blocking call"}

@app.get("/health")
async def health() -> dict[str,str]:
    return {"status":"ok"}