from fastapi import APIRouter
from pydantic import BaseModel
from src.services.generation_service import generate_answer

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("")
def get_answer(data: QueryRequest):
    answer, retrival_docs = generate_answer(data.query)
    return {
        "answer": answer,
        "retrieval_documents": retrival_docs
    }

if __name__ == "__main__":
    answer, retrival_docs = generate_answer("abc")
    print(answer)
    print(retrival_docs)