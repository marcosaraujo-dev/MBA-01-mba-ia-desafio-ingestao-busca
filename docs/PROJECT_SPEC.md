# Especificação Técnica — Semantic PDF Search

## 1. Visão Geral

### Descrição

Sistema responsável por realizar ingestão de documentos PDF, gerar embeddings e armazenar informações em banco vetorial PostgreSQL utilizando pgVector.

Após a ingestão, o usuário poderá realizar consultas via terminal e obter respostas baseadas exclusivamente no conteúdo do documento.

---

## 2. Objetivos

### Objetivo principal

Desenvolver um mecanismo de busca semântica baseado em embeddings.

### Objetivos específicos

- Ler arquivos PDF
- Dividir conteúdo em chunks
- Gerar embeddings
- Persistir vetores no PostgreSQL
- Recuperar conteúdo relevante
- Responder perguntas através de LLM
- Impedir uso de conhecimento externo

---

## 3. Requisitos Funcionais

### RF01 — Ingestão do PDF

O sistema deve:

- Carregar arquivo PDF
- Extrair texto
- Dividir em chunks
- Gerar embeddings
- Salvar vetores

---

### RF02 — Divisão do documento

Parâmetros obrigatórios:

| Propriedade | Valor |
|-------------|--------|
| Chunk Size | 1000 |
| Overlap | 150 |

---

### RF03 — Consulta

O sistema deve:

- Receber perguntas via CLI
- Vetorizar pergunta
- Buscar 10 resultados relevantes
- Construir contexto
- Chamar LLM
- Retornar resposta

---

### RF04 — Similaridade

Busca:

```python
similarity_search_with_score(
    query,
    k=10
)
```

---

## 4. Regras de Negócio

### RN01

Responder exclusivamente usando conteúdo do PDF.

---

### RN02

Caso não exista informação suficiente:

```txt
Não tenho informações necessárias para responder sua pergunta.
```

---

### RN03

Não utilizar conhecimento externo.

---

### RN04

Não criar interpretações ou opiniões.

---

## 5. Arquitetura

### Fluxo de ingestão

```txt
PDF
 ↓
PyPDFLoader
 ↓
RecursiveCharacterTextSplitter
 ↓
Embeddings
 ↓
PGVector
 ↓
PostgreSQL
```

---

### Fluxo de consulta

```txt
Pergunta do usuário
 ↓
Embedding da pergunta
 ↓
Similarity Search
 ↓
Top 10 resultados
 ↓
Construção do Prompt
 ↓
LLM
 ↓
Resposta
```

---

## 6. Tecnologias

| Tecnologia | Utilização |
|-------------|------------|
| Python | Linguagem |
| LangChain | Orquestração |
| PostgreSQL | Persistência |
| pgVector | Vetores |
| Docker | Infraestrutura |
| OpenAI | Embeddings/LLM |
| Gemini | Embeddings/LLM |

---

## 7. Estrutura do Projeto

```txt
src/
├── ingest.py
├── search.py
└── chat.py
```

---

## 8. Componentes

### ingest.py

Responsável por:

- Carregar PDF
- Dividir texto
- Gerar embeddings
- Persistir dados

---

### search.py

Responsável por:

- Receber consulta
- Executar busca vetorial
- Retornar contexto

---

### chat.py

Responsável por:

- Interação CLI
- Construção do prompt
- Chamada da LLM

---

## 9. Prompt utilizado

```txt
CONTEXTO:

{resultados}

REGRAS:

- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
"Não tenho informações necessárias para responder sua pergunta."

- Nunca invente informações.
- Nunca utilize conhecimento externo.

PERGUNTA DO USUÁRIO:

{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
```

---

## 10. Melhorias futuras

- Interface Web
- Upload múltiplo de PDFs
- Histórico de consultas
- Cache de embeddings
- Reranking
- Testes automatizados
- Containerização completa
