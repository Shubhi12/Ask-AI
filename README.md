# ASK AI

## Enterprise AI Knowledge Assistant

ASK AI is a multi-tenant, RAG-powered knowledge assistant that enables companies to make their internal knowledge easily accessible through an embeddable **Ask AI** interface.

Organizations can upload and manage internal documents, while users can ask questions in natural language and receive context-aware answers based on the organization's knowledge base.

The system uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from company documents and provide grounded responses using a Large Language Model (LLM).

---

# 🚀 Features

## 📄 Document Ingestion

Organizations can upload documents to build their knowledge base.

Supported capabilities include:

* Document upload
* Text extraction
* Document parsing
* Text chunking
* Embedding generation
* Vector storage
* Asynchronous document processing
* Document processing status tracking

### Ingestion Flow

```text
Upload Document
       │
       ▼
Store Document
       │
       ▼
Extract Text
       │
       ▼
Split into Chunks
       │
       ▼
Generate Embeddings
       │
       ▼
Store Vectors
       │
       ▼
Document Ready for Search
```

---

# 💬 Ask AI

Users can ask questions about their organization's knowledge base through the ASK AI interface.

Example:

```text
How many paid leaves do employees receive?
```

ASK AI retrieves relevant information from the organization's documents and generates a response based on the retrieved context.

### Query Flow

```text
User Question
       │
       ▼
Query Processing
       │
       ▼
Generate Query Embedding
       │
       ▼
Retrieve Relevant Documents
       │
       ▼
Rerank Results
       │
       ▼
Build Context
       │
       ▼
LLM
       │
       ▼
Generate Answer
       │
       ▼
Answer + Sources
```

---

# 🏢 Multi-Tenant Architecture

ASK AI is designed as a multi-tenant platform.

Each organization has its own isolated knowledge base.

```text
Organization A
│
├── HR Policies
├── Engineering Documentation
└── Employee Handbook


Organization B
│
├── Product Documentation
└── Customer Policies
```

When a user asks a question, ASK AI retrieves information only from documents belonging to that organization.

```text
User Query
    │
    ▼
Identify Organization
    │
    ▼
Apply Tenant Filter
    │
    ▼
Search Organization Knowledge Base
```

This ensures proper tenant isolation and prevents data from one organization from being accessed by another.

---

# 🧠 RAG Architecture

ASK AI uses a Retrieval-Augmented Generation pipeline.

```text
                    ┌─────────────────────┐
                    │     User Query      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Query Processing  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Retrieval      │
                    │                     │
                    │ Vector Search       │
                    │ Keyword Search      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Reranking      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Context Builder   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │        LLM          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Answer + Sources    │
                    └─────────────────────┘
```

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │    ASK AI Widget    │
                         │                     │
                         │   💬 Ask a question │
                         └──────────┬──────────┘
                                    │
                                    ▼
                           ┌────────────────┐
                           │   FastAPI API  │
                           └────────┬───────┘
                                    │
                   ┌────────────────┴────────────────┐
                   │                                 │
                   ▼                                 ▼

          ┌──────────────────┐              ┌──────────────────┐
          │ Document Service │              │    RAG Service   │
          └────────┬─────────┘              └────────┬─────────┘
                   │                                 │
                   ▼                                 ▼

          ┌──────────────────┐              ┌──────────────────┐
          │ Ingestion Worker │              │ Query Pipeline   │
          └────────┬─────────┘              └────────┬─────────┘
                   │                                 │
                   ▼                                 ▼

          ┌──────────────────┐              ┌──────────────────┐
          │ PostgreSQL       │              │ Vector Search    │
          │ Metadata         │              │ pgvector         │
          └──────────────────┘              └──────────────────┘
```

---

# 🛠️ Technology Stack

## Backend

* Python
* FastAPI
* SQLAlchemy

## Database

* PostgreSQL
* pgvector

## Background Processing

* Celery
* Redis

## AI & RAG

* Large Language Models (LLMs)
* Embeddings
* Vector Search
* Retrieval-Augmented Generation (RAG)

## Frontend

* React
* TypeScript

## Infrastructure

* Docker
* Docker Compose

---

# 📂 Project Structure

```text
ask-ai/
│
├── backend/
│   ├── app/
│   │
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── documents.py
│   │   │       ├── queries.py
│   │   │       └── conversations.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   │
│   │   ├── models/
│   │   │
│   │   ├── schemas/
│   │   │
│   │   ├── repositories/
│   │   │
│   │   ├── services/
│   │   │
│   │   ├── ingestion/
│   │   │   ├── loaders/
│   │   │   ├── chunking/
│   │   │   ├── embeddings/
│   │   │   └── pipeline.py
│   │   │
│   │   ├── rag/
│   │   │   ├── retrieval/
│   │   │   ├── generation/
│   │   │   ├── query/
│   │   │   └── pipeline.py
│   │   │
│   │   └── main.py
│   │
│   └── tests/
│
├── widget/
│
├── docs/
│   ├── architecture.md
│   ├── api-design.md
│   └── rag-pipeline.md
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

# ⚙️ Core Components

## Document Ingestion Pipeline

Responsible for converting uploaded documents into searchable knowledge.

```text
Document
   │
   ▼
Loader
   │
   ▼
Text Extraction
   │
   ▼
Chunking
   │
   ▼
Embedding Generation
   │
   ▼
Vector Storage
```

---

## Retrieval Pipeline

Responsible for finding relevant information.

Capabilities:

* Semantic search
* Vector similarity search
* Keyword search
* Hybrid search
* Metadata filtering
* Tenant-based filtering

---

## Reranking

Retrieved documents may not always be equally relevant.

ASK AI uses a reranking layer to select the most relevant chunks before sending context to the LLM.

```text
Top 10 Retrieved Chunks
          │
          ▼
       Reranker
          │
          ▼
Top 3 Relevant Chunks
          │
          ▼
         LLM
```

---

## Answer Generation

The LLM receives:

* User question
* Retrieved context
* System instructions

The model generates an answer grounded in the provided company knowledge.

If sufficient information is not available, the system should avoid generating unsupported answers.

Example:

```text
I couldn't find enough information in the available documents to answer this question.
```

---

# 🔐 Security and Tenant Isolation

ASK AI is designed with tenant isolation in mind.

Every request is associated with an organization.

```text
Request
   │
   ▼
Authenticate User
   │
   ▼
Identify Organization
   │
   ▼
Apply Organization Filter
   │
   ▼
Retrieve Authorized Knowledge Only
```

The system ensures that:

* Users can access only authorized data.
* Documents are isolated by organization.
* Vector searches are filtered by tenant.
* Conversations belong to the appropriate organization.

---

# 🧩 Embeddable ASK AI Widget

ASK AI is designed to be integrated into a company's application through an embeddable widget.

Example:

```text
┌─────────────────────────────┐
│ 💬 ASK AI                   │
│                             │
│ Ask a question...           │
│                             │
│ How do I apply for leave?   │
│                             │
│ ─────────────────────────── │
│                             │
│ You can apply for leave...  │
│                             │
│ 📄 Employee Leave Policy    │
└─────────────────────────────┘
```

The goal is to allow organizations to integrate ASK AI directly into their existing applications.

---

# 🔮 Future Improvements

Planned improvements include:

* [ ] Hybrid search
* [ ] Query rewriting
* [ ] Reranking
* [ ] Conversation-aware retrieval
* [ ] Streaming LLM responses
* [ ] Document source citations
* [ ] Role-based access control
* [ ] User feedback on responses
* [ ] RAG evaluation pipeline
* [ ] Response confidence scoring
* [ ] Observability and tracing
* [ ] Support for additional document formats
* [ ] API key management
* [ ] Widget customization

---

# 🎯 Project Goals

The goal of ASK AI is to demonstrate how a production-oriented AI application can combine:

* Backend engineering
* API design
* Asynchronous processing
* Multi-tenant architecture
* Retrieval-Augmented Generation
* Vector databases
* LLM integration

Rather than being a simple chatbot, ASK AI is designed as an extensible knowledge platform that organizations can integrate into their applications.

---

# 👩‍💻 Author

**Saloni Sahu**

Senior Software Developer | AI & LLM Enthusiast

---

# 📌 Status

🚧 **Currently under active development**

The project is being built incrementally, starting with the core document ingestion and RAG query pipelines.
