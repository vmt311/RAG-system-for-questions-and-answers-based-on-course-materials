from tqdm import tqdm
import uuid
from utils.config import settings
from langchain_huggingface import HuggingFaceEmbeddings
from src.database.chromadb import document_collection, chroma_client, COLLECTION_NAME
from src.services.data_preparation_service import create_documents_from_file_excel

EMBEDDING_MODEL = settings.BI_ENCODER_MODEL

def embed_document(docs):
    
    model_embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    documents_ls = []
    metadatas_ls = []
    ids_ls = []
    embeddings_ls = []

    for doc in tqdm(docs):
        documents_ls.append(doc.page_content)
        metadatas_ls.append(doc.metadata)
        ids_ls.append(str(uuid.uuid4()))
        embeddings_ls.append(model_embedding.embed_query("passage: " + doc.page_content))

    document_collection.add(
        documents=documents_ls,
        embeddings=embeddings_ls,
        metadatas=metadatas_ls,
        ids=ids_ls
    )

    print('Write Vector DB done')

def clear_collection():

    chroma_client.delete_collection(name=COLLECTION_NAME)
    print('Clear collection done')

if __name__ == "__main__":
    # docs = ['data/lek1.xlsx', 'data/lek2.xlsx', 'data/lek3.xlsx', 'data/lek4.xlsx', 'data/lek5.xlsx']
    # for doc in docs:
    #     doc_created = create_documents_from_file_excel(doc)
    #     embed_document(doc_created)
    #     print(f'writed {doc}')
    clear_collection()
