import pandas as pd
from langchain_community.document_loaders import DataFrameLoader
from langchain_core.documents import Document
import utils.functions as fct

# Create document from file excel
def create_documents_from_file_excel(path_excel):
    df = pd.read_excel(path_excel)
    df = df[['Fact', 'Source']]
    loader = DataFrameLoader(df, page_content_column="Fact")
    docs = loader.load()

    documents = []
    for doc in docs:
        preprocess_page_content = fct.preprocess_text(doc.page_content)
        metadata = {
                    'Source': doc.metadata['Source'],
                    'Raw': doc.page_content
                }
        
        doc_tmp = Document(page_content=preprocess_page_content, metadata=metadata)
        documents.append(doc_tmp)
    print(path_excel)
    return documents

if __name__ == "__main__":
    documents = create_documents_from_file_excel('data/lek1.xlsx')