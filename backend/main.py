import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import answer_api, stt_api

app = FastAPI(title="aRAG API", version="1.0")

origins = [
    # url of frontend server
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(answer_api.router, prefix="/llm", tags=["llm"])
app.include_router(stt_api.router, prefix="/speech-to-text", tags=["speech-to-text"])

@app.get("/")
def root():
    print("DEBUG: Modified version called")
    return {"message": "Welcome Thien to RAG"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080, reload=True)