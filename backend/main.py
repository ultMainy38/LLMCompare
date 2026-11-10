import httpx
import asyncio
import uvicorn, os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel

CACHED_MODELS = None

class ChatRequest(BaseModel):
    message: str
    models: list[str]


async def query_model(model: str, task: str):
    try:
        url = "https://llm.codex.so/generate"
        headers = {"x-api-key": os.getenv("LLM_API_KEY"), "Content-Type": "application/json"}
        payload = {"prompt": task, "model": model}

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        answer = data.get("text", "")
        return {"model": model, "content": answer, "error": None}
    except Exception as e:
        return {"model": model, "content": None, "error": str(e)}


load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/models")
async def figure_out_models():
    global CACHED_MODELS
    if CACHED_MODELS is not None:
        return {"models": CACHED_MODELS, "cached": True}
    else:
        try:
            headers = {"x-api-key": os.getenv("LLM_API_KEY")}
            async with httpx.AsyncClient() as client:
                response = await client.get("https://llm.codex.so/models", headers=headers)
            data = response.json()
            CACHED_MODELS = [model["id"] for model in data.get("models", [])]
            return {"models": CACHED_MODELS, "cached": False}
        except Exception as e:
            return {"error": str(e)}


@app.post("/api/chat")
async def get_answers(request: ChatRequest):
    tasks = [query_model(model, request.message) for model in request.models]
    result = await asyncio.gather(*tasks, return_exceptions=True)
    return {"answers": result}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)