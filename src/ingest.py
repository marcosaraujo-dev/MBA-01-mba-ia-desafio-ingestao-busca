import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL")

BATCH_SIZE = 5
BATCH_DELAY_SECONDS = 4


def ingest_pdf():
    print(f"Carregando PDF: {PDF_PATH}")
    loader = PyPDFLoader(PDF_PATH)
    pages = loader.load()
    print(f"  {len(pages)} página(s) carregada(s)")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )
    chunks = splitter.split_documents(pages)
    print(f"  {len(chunks)} chunk(s) gerado(s)")

    print("Inicializando banco vetorial...")
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

    # Cria a coleção vazia (limpa se já existir)
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
        pre_delete_collection=True,
    )

    total_batches = (len(chunks) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"Gerando embeddings em {total_batches} lote(s) de {BATCH_SIZE}...")

    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        print(f"  Lote {batch_num}/{total_batches} ({len(batch)} chunks)...")
        vector_store.add_documents(batch)

        if i + BATCH_SIZE < len(chunks):
            time.sleep(BATCH_DELAY_SECONDS)

    print(f"Ingestão concluída: {len(chunks)} chunks armazenados em '{COLLECTION_NAME}'.")


if __name__ == "__main__":
    ingest_pdf()
