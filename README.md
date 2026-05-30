# Semantic PDF Search

Sistema de busca semântica em documentos PDF utilizando LangChain, PostgreSQL + pgVector e Google Gemini.

Após a ingestão, o usuário realiza perguntas via terminal e recebe respostas baseadas **exclusivamente** no conteúdo do documento.

---

## Tecnologias

| Tecnologia | Uso |
|------------|-----|
| Python 3.11+ | Linguagem |
| LangChain | Orquestração do pipeline RAG |
| PostgreSQL + pgVector | Banco vetorial |
| Docker | Infraestrutura do banco |
| Google Gemini | Embeddings e LLM |

---

## Estrutura do projeto

```
.
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── document.pdf
├── README.md
├── docs/
│   └── PROJECT_SPEC.md
└── src/
    ├── ingest.py
    ├── search.py
    └── chat.py
```

---

## Pré-requisitos

- Python 3.11 ou superior
- Docker Desktop instalado e em execução
- Chave de API do Google AI Studio (gratuita): https://aistudio.google.com

---

## Configuração

### 1. Clonar o repositório

```bash
git clone <repositorio>
cd <repositorio>
```

### 2. Criar e ativar o ambiente virtual

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Copie o arquivo de exemplo e preencha com sua chave:

```bash
cp .env.example .env
```

Edite o `.env` com os valores abaixo:

```env
GOOGLE_API_KEY=sua_chave_aqui
GOOGLE_EMBEDDING_MODEL=models/gemini-embedding-001
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=pdf_documents
PDF_PATH=document.pdf
```

> **Nota:** Se você já tiver um PostgreSQL local rodando na porta 5432, altere a porta no `docker-compose.yml` e na `DATABASE_URL` para `5433` (ou outra disponível).

---

## Execução

### 1. Subir o banco de dados

```bash
docker compose up -d
```

### 2. Ingerir o PDF

Execute uma única vez para processar o documento e armazenar os vetores:

```bash
python src/ingest.py
```

Saída esperada:
```
Carregando PDF: document.pdf
  34 página(s) carregada(s)
  67 chunk(s) gerado(s)
Inicializando banco vetorial...
Gerando embeddings em 14 lote(s) de 5...
  Lote 1/14 (5 chunks)...
  ...
Ingestão concluída: 67 chunks armazenados em 'pdf_documents'.
```

### 3. Iniciar o chat

```bash
python src/chat.py
```

---

## Exemplos de uso

**Pergunta sobre conteúdo do documento:**
```
Você: Qual o faturamento da empresa Alfa Energia S.A.?

Assistente: O faturamento da empresa Alfa Energia S.A. é R$ 722.875.391,46.
```

**Pergunta fora do contexto:**
```
Você: Qual a capital da França?

Assistente: Não tenho informações necessárias para responder sua pergunta.
```

Para encerrar o chat, digite `sair` ou pressione `Ctrl+C`.

---

## Observações

- O sistema responde **somente** com base no conteúdo do PDF ingerido.
- Conhecimento externo da LLM é bloqueado pelas regras do prompt.
- O modelo de embedding utilizado é `gemini-embedding-001`.
- O modelo de chat utilizado é `gemini-2.5-flash`.
