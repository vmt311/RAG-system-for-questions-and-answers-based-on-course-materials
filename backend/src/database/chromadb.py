import chromadb

HOST = 'localhost'
PORT = '8000'
COLLECTION_NAME = 'collection_test'
chroma_client = chromadb.HttpClient(host=HOST, port=PORT)
document_collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)