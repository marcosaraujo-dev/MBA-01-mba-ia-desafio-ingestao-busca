# Semantic PDF Search

Sistema para ingestão de documentos PDF e busca semântica utilizando LangChain, PostgreSQL + pgVector e LLM.

## Objetivo

Realizar ingestão de um arquivo PDF, armazenar embeddings em banco vetorial e permitir consultas via terminal (CLI), retornando respostas baseadas exclusivamente no conteúdo do documento.

---

## Tecnologias utilizadas

- Python
- LangChain
- PostgreSQL
- pgVector
- Docker
- OpenAI ou Gemini

---

## Estrutura do projeto

```txt
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

## Configuração do ambiente

### 1. Clonar projeto

```bash
git clone <repositorio>
cd <repositorio>
```

### 2. Criar ambiente virtual

Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```cmd
python -m venv venv
venv\Scripts\activate
```

---

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 4. Configurar variáveis de ambiente

Copie:

```bash
cp .env.example .env
```

Editar:

```env
OPENAI_API_KEY=sua_chave
```

ou:

```env
GOOGLE_API_KEY=sua_chave
```

---

## Execução

### Subir PostgreSQL

```bash
docker compose up -d
```

---

### Executar ingestão do PDF

```bash
python src/ingest.py
```

---

### Executar chat

```bash
python src/chat.py
```

---

## Exemplo de utilização

Pergunta:

```txt
Qual o faturamento da Empresa SuperTechIABrazil?
```

Resposta:

```txt
O faturamento foi de 10 milhões de reais.
```

---

Pergunta fora do contexto:

```txt
Qual a capital da França?
```

Resposta:

```txt
Não tenho informações necessárias para responder sua pergunta.
```

---

## Observações

O sistema utiliza somente informações presentes no PDF.

Não utiliza conhecimento externo da LLM.
