from src.services.retrieval_service import get_retrieval_documents
from utils.config import settings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain_deepseek import ChatDeepSeek

OLLAMA_LLM = settings.OLLAMA_LLM

# LLM cấu hình (model chạy bằng vLLM)
VLLM_MODEL_NAME = settings.VLLM_MODEL_NAME
VLLM_BASE_URL = settings.VLLM_BASE_URL

# DEEPSEEK_LLM = ChatDeepSeek(
#         model="deepseek-chat",
#         api_key=settings.DEEPSEEK_API_KEY,
#         api_base="https://api.deepseek.com",
#         max_tokens=1024
#     )

def generate_answer(query):
    print(OLLAMA_LLM)
    retrival_docs = get_retrieval_documents(query)
    contexts = []
    for i, doc in enumerate(retrival_docs, start=1):
        reliability = "надежный источник" if doc['flag'] == "True" else "ненадежный источник (может содержать ошибки)"
        formatted_context = f"[Документ {i} - {reliability}]:\n{doc['context']}"
        contexts.append(formatted_context)
        
    if not contexts:
        default_response = (
            f"К сожалению, по вашему запросу: \"{query}\"\n"
            "не удалось найти соответствующую информацию в конспектах лекций. "
            "Попробуйте переформулировать вопрос или задать другой."
        )
        # print(default_response)
        return default_response, retrival_docs

    prompt_with_reliable = PromptTemplate.from_template(
    """
    Вы — преподаватель университета, ведущий курс "Интеллектуальные системы и технологии". 
    Ваш студент задал Вам следующий вопрос:\n"{query}"\n

    Пожалуйста, дайте развернутый ответ, используя выдержки из лекционных материалов ниже. 
    Каждая выдержка помечена как надежная или ненадежная. 
    Постарайтесь в первую очередь опираться на надежные источники. 
    Ненадежные источники можно использовать с осторожностью.

    Вот выдержки:\n{contexts}\n
    """
    )

    prompt_all_unreliable = PromptTemplate.from_template(
    """
    Вы — преподаватель университета, ведущий курс "Интеллектуальные системы и технологии". 
    Ваш студент задал Вам следующий вопрос:\n"{query}"\n

    К сожалению, в лекционных материалах не найдено надежных источников по этому вопросу. 
    Тем не менее, ниже представлены ненадежные выдержки, которые могут содержать ошибки.

    Пожалуйста, дайте ответ, основываясь на Ваших знаниях, 
    и, если возможно, используйте представленные выдержки с осторожностью.

    Вот выдержки:\n{contexts}\n
    """
    )

    all_unreliable = all(doc['flag'] == "False" for doc in retrival_docs)
    prompt_template = prompt_all_unreliable if all_unreliable else prompt_with_reliable

    llm_ollama = OllamaLLM(model=OLLAMA_LLM)

    # vllm = ChatOpenAI(
    #     base_url=VLLM_BASE_URL,
    #     api_key="fake_key",
    #     model=VLLM_MODEL_NAME
    # )

    chain = prompt_template | llm_ollama

    answer = chain.invoke(
        {
            'contexts': contexts,
            'query': query
        }
    )
    print(answer)
    # return answer.content, retrival_docs
    return answer, retrival_docs

if __name__ == "__main__":
    query = "Свойства сильного искусственного интеллекта?"
    generate_answer(query)