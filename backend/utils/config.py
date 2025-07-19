from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CHROMA_DB_PATH: str = "./chromadb_store"
    DATASTORAGE: str = "data/pdfs"
    # BI_ENCODER_MODEL: str = "cointegrated/LaBSE-en-ru"
    # BI_ENCODER_MODEL: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    # BI_ENCODER_MODEL: str = "DiTy/bi-encoder-russian-msmarco"
    BI_ENCODER_MODEL: str = "deepvk/USER-base"
    CROSS_ENCODER_MODEL: str = "DiTy/cross-encoder-russian-msmarco"
    # CROSS_ENCODER_MODEL: str = "deepvk/USER-bge-m3"
    # CROSS_ENCODER_MODEL: str = "intfloat/multilingual-e5-large-instruct"
    # CROSS_ENCODER_MODEL: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    OLLAMA_LLM: str = "bambucha/saiga-llama3"
    # OLLAMA_LLM: str = "deepseek-r1:14b"
    # DEEPSEEK_API_KEY: str = ""
    VLLM_BASE_URL: str = "http://localhost:8000/v1"
    VLLM_MODEL_NAME: str = "mistralai/Mistral-7B-Instruct-v0.2"
settings = Settings()