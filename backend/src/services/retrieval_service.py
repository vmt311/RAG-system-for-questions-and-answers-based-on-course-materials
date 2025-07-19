from utils.config import settings
from src.database.chromadb import chroma_client, COLLECTION_NAME
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder
from src.services.vectordb_service import clear_collection, create_documents_from_file_excel, embed_document

import pandas as pd

EMBEDDING_MODEL = settings.BI_ENCODER_MODEL
CROSS_MODEL = settings.CROSS_ENCODER_MODEL


def load_data_from_vectordb():
    db_load = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=HuggingFaceEmbeddings(model_name = EMBEDDING_MODEL),
        client=chroma_client
    )

    return db_load

def search_similarity(query: str, top_k=10):
    db_load = load_data_from_vectordb()
    similar_docs = db_load.similarity_search(query="query: " + query, k=top_k)
    return similar_docs

def search_reranking_senmatic(similar_docs, query, top_k=5):
    pairs = [[query, doc.page_content] for doc in similar_docs]
    cross_model = CrossEncoder(CROSS_MODEL)
    scores = [float(score) for score in cross_model.predict(pairs)]

    similar_docs_with_score = list(zip(similar_docs, scores))
    sorted_docs = sorted(similar_docs_with_score, key=lambda x:x[1], reverse=True)

    return sorted_docs[:top_k]

def get_retrieval_documents(query: str, first_rank=10, final_rank=5):
    similar_docs = search_similarity(query, first_rank)
    retrival_docs = search_reranking_senmatic(similar_docs, query, final_rank)
    result = []

    for doc, score in retrival_docs:
        tmp = dict()
        tmp['context'] = doc.page_content
        tmp['score'] = score
        tmp['source'] = doc.metadata['Source']
        if score >= 0.6:
            tmp['flag'] = "True"
        else:
            tmp['flag'] = "False"

        result.append(tmp)
    return result

if __name__ == "__main__":

    query_list = [
        'Что такое агент в искусственном интеллекте?',
        'Назовите три основных свойства агента.',
        'Что означает термин "сильный ИИ"?',
        'Что такое Modus ponens в логике высказываний?',
        'Приведите пример предиката из логики предикатов.',
        'Что такое "онтология" в контексте ИИ?',
        'Какие типы окружающих сред существуют в ИИ?',
        'Что такое "резолюция" в логике высказываний?',
        'Что означает термин "полиномиальная сложность"?',
        'Назовите этапы создания онтологии.'
    ]

    excel_filename = "data/results_new.xlsx"

    with pd.ExcelWriter(excel_filename, engine="openpyxl", mode="w") as writer:  # Ghi mới file
        for i, query in enumerate(query_list, start=1):  # Bắt đầu từ Sheet1
            result_list = get_retrieval_documents(query, 20, 20)

            df = pd.DataFrame(result_list)
            df.insert(0, "Query", query)  # Thêm cột Query

            # Ghi vào Excel với sheet_name là Sheet1, Sheet2, Sheet3,...
            sheet_name = f"Sheet{i}"
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Results saved to {excel_filename}")