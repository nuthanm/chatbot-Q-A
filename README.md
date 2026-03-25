# 🤖 Chatbot Q&A — Document Intelligence Assistant

> Upload your document and get instant answers using our AI-powered chatbot.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-latest-green)](https://python.langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?logo=openai)](https://platform.openai.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 Table of Contents

1. [What Is This App?](#-what-is-this-app)
2. [Features](#-features)
3. [Architecture Overview](#-architecture-overview)
4. [Tech Stack & Libraries](#-tech-stack--libraries)
5. [Prerequisites](#-prerequisites)
6. [Getting API Tokens](#-getting-api-tokens)
7. [Environment Variables](#-environment-variables)
8. [Installation & Setup](#-installation--setup)
9. [How to Run](#-how-to-run)
10. [Usage Guide](#-usage-guide)
11. [Project Structure](#-project-structure)
12. [Reference Links](#-reference-links)
13. [Contributing](#-contributing)

---

## 🧠 What Is This App?

**Chatbot Q&A** is an AI-powered document question-answering application. You upload any document (PDF, Word, TXT, etc.), and our chatbot reads and understands it so you can ask questions in plain English and get accurate, context-aware answers — no manual searching required.

This is built on the **RAG (Retrieval-Augmented Generation)** pattern:
1. Your document is broken into chunks and stored in a vector database.
2. When you ask a question, the most relevant chunks are retrieved.
3. A Large Language Model (LLM) uses those chunks to craft a precise answer.

---

## ✨ Features

- 📄 **Multi-format document upload** — PDF, DOCX, TXT supported
- 💬 **Conversational Q&A** — Ask follow-up questions naturally
- 🔍 **Semantic search** — Finds relevant context even if exact words differ
- 🧩 **Modular architecture** — Easy to swap LLM provider or vector store
- 🔐 **Secure** — API keys stored in environment variables, never committed

---

## 🏗️ Architecture Overview

```
User
 │
 ▼
[Streamlit UI]
 │  Upload Document        Ask Question
 ▼                              │
[Document Loader]         [Question Embedder]
 │                              │
 ▼                              ▼
[Text Splitter]  ──►  [Vector Store (FAISS/Chroma)]
                              │
                              ▼ (top-k similar chunks)
                       [LLM (OpenAI / Azure OpenAI)]
                              │
                              ▼
                          [Answer]
```

---

## 🛠️ Tech Stack & Libraries

| Layer | Library / Tool | Purpose |
|-------|---------------|---------|
| **UI** | [Streamlit](https://streamlit.io/) | Web interface for file upload and chat |
| **LLM Orchestration** | [LangChain](https://python.langchain.com/) | Chains, prompts, retrieval |
| **LLM Provider** | [OpenAI](https://platform.openai.com/) / [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) | GPT-4 / GPT-3.5 models |
| **Embeddings** | [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings) | Convert text to vectors |
| **Vector Store** | [FAISS](https://faiss.ai/) / [Chroma](https://www.trychroma.com/) | Store and retrieve document vectors |
| **Document Loaders** | [PyPDFLoader](https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf) / [Docx2txtLoader](https://python.langchain.com/docs/integrations/document_loaders/docx2txt) | Parse documents |
| **Text Splitting** | LangChain `RecursiveCharacterTextSplitter` | Chunk documents intelligently |
| **Environment** | [python-dotenv](https://pypi.org/project/python-dotenv/) | Load secrets from `.env` |

### Install all dependencies

```bash
pip install -r requirements.txt
```

Key packages in `requirements.txt`:

```
langchain
langchain-openai
langchain-community
openai
streamlit
faiss-cpu
chromadb
pypdf
docx2txt
python-dotenv
tiktoken
```

---

## ✅ Prerequisites

Before you begin, make sure you have the following installed:

| Requirement | Version | Download |
|-------------|---------|----------|
| Python | 3.10 or higher | [python.org](https://www.python.org/downloads/) |
| pip | Latest | Bundled with Python |
| Git | Any | [git-scm.com](https://git-scm.com/) |
| (Optional) VS Code | Latest | [code.visualstudio.com](https://code.visualstudio.com/) |

Verify your Python version:

```bash
python --version   # Should print Python 3.10.x or higher
```

---

## 🔑 Getting API Tokens

### OpenAI API Key

1. Go to [https://platform.openai.com/](https://platform.openai.com/) and sign in (or create a free account).
2. Navigate to **API Keys** → **Create new secret key**.
3. Copy the key — you will **not** be able to see it again.
4. Billing: Check [OpenAI pricing](https://openai.com/pricing). Free-tier credits are available for new accounts.

### Azure OpenAI (Alternative)

If you are using **Azure OpenAI** instead of the direct OpenAI API:

1. Go to [Azure Portal](https://portal.azure.com/) → **Azure OpenAI** → Create a resource.
2. Once created, go to **Keys and Endpoint** to find your `API_KEY` and `ENDPOINT`.
3. Deploy a model (e.g., `gpt-4`, `gpt-35-turbo`) under **Model Deployments**.
4. Note your **Deployment Name** — you will need it in the config.

---

## 🌍 Environment Variables

Create a `.env` file in the project root (this file is **already in `.gitignore`** — never commit it):

```env
# ── OpenAI Direct ──────────────────────────────────────
OPENAI_API_KEY=sk-your-openai-key-here

# ── Azure OpenAI (use instead of the above if on Azure) ─
AZURE_OPENAI_API_KEY=your-azure-openai-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-01

# ── Vector Store ────────────────────────────────────────
VECTOR_STORE=faiss          # options: faiss | chroma

# ── App Settings ────────────────────────────────────────
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_TOKENS=1000
```

> ⚠️ **Security note:** Never share your `.env` file or commit it to version control.

---

## 📦 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/nuthanm/chatbot-Q-A.git
cd chatbot-Q-A
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
# Copy the example file and fill in your values
cp .env.example .env
# Now open .env and add your API keys
```

---

## ▶️ How to Run

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` — the app will load automatically.

---

## 📚 Usage Guide

1. **Upload a document** — Click "Browse files" and select a PDF, DOCX, or TXT file.
2. **Wait for processing** — The app chunks and indexes the document (a few seconds).
3. **Ask a question** — Type your question in the chat box and press Enter.
4. **Read the answer** — The chatbot responds with a context-grounded answer.
5. **Follow-up questions** — The conversation is maintained; ask as many follow-ups as you like.
6. **Upload a new document** — Click "Clear & Upload New" to start fresh.

---

## 📂 Project Structure

```
chatbot-Q-A/
├── app.py                  # Streamlit entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Template for environment variables
├── .gitignore
├── README.md
│
├── src/
│   ├── document_loader.py  # Load and parse uploaded files
│   ├── text_splitter.py    # Chunk documents into pieces
│   ├── embeddings.py       # Create vector embeddings
│   ├── vector_store.py     # Store/retrieve vectors (FAISS or Chroma)
│   ├── llm_chain.py        # LangChain QA chain setup
│   └── utils.py            # Helper utilities
│
└── tests/
    └── test_*.py           # Unit tests
```

> 📝 The structure above reflects the intended layout. Update this section as the project grows.

---

## 🔗 Reference Links

### Official Documentation

| Resource | URL |
|----------|-----|
| LangChain Docs | https://python.langchain.com/docs/ |
| LangChain RAG Tutorial | https://python.langchain.com/docs/tutorials/rag/ |
| OpenAI API Reference | https://platform.openai.com/docs/api-reference |
| OpenAI Embeddings Guide | https://platform.openai.com/docs/guides/embeddings |
| Azure OpenAI Service | https://learn.microsoft.com/en-us/azure/ai-services/openai/ |
| Streamlit Docs | https://docs.streamlit.io/ |
| FAISS GitHub | https://github.com/facebookresearch/faiss |
| Chroma Docs | https://docs.trychroma.com/ |
| python-dotenv | https://pypi.org/project/python-dotenv/ |

### Learning Resources

| Topic | URL |
|-------|-----|
| What is RAG? | https://aws.amazon.com/what-is/retrieval-augmented-generation/ |
| LangChain RAG from Scratch | https://github.com/langchain-ai/rag-from-scratch |
| OpenAI Cookbook | https://cookbook.openai.com/ |
| LangChain Q&A over Documents | https://python.langchain.com/docs/tutorials/rag/ |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> 💡 **Tip:** Keep this README up to date as you add new features, change libraries, or update configuration options. A well-maintained README is the best onboarding guide for new contributors and your future self.

