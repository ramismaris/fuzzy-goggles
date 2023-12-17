import json

import httpx

from web.config import MODEL_API_URL


async def get_model_answer(body: dict) -> dict | None:
    body = json.loads(json.dumps(body, default=str, ensure_ascii=False))
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{MODEL_API_URL}/generate", json=body, timeout=None)

    if res.status_code != 200:
        return None

    return res.json()
