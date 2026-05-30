import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_postgres import PGVector
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL")

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def _build_context(docs_with_scores: list) -> str:
    return "\n\n".join(doc.page_content for doc, _score in docs_with_scores)


def search_prompt(question: str | None = None):
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

        vector_store = PGVector(
            embeddings=embeddings,
            collection_name=COLLECTION_NAME,
            connection=DATABASE_URL,
        )

        prompt = PromptTemplate(
            input_variables=["contexto", "pergunta"],
            template=PROMPT_TEMPLATE,
        )

        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

        def retrieve_context(inputs: dict) -> dict:
            results = vector_store.similarity_search_with_score(inputs["pergunta"], k=10)
            return {
                "contexto": _build_context(results),
                "pergunta": inputs["pergunta"],
            }

        chain = RunnablePassthrough() | retrieve_context | prompt | llm | StrOutputParser()
        return chain

    except Exception as e:
        print(f"Erro ao inicializar search_prompt: {e}")
        return None
