from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn, os

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def check_health():
    if os.getenv("LLM_API_TOKEN") is not None:
        return {"status": "ok"}
    return {"status": "not ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)