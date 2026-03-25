# chatbot-Q-A

Upload your PDF documents and get instant answers using our AI-powered chatbot.

## Features

- 📄 Upload one or more PDF files
- 🔍 Intelligent text extraction using **pdfplumber**
- 🧠 Semantic search powered by **FAISS** vector store and **OpenAI Embeddings**
- 💬 Conversational Q&A with chat history via **LangChain** + **OpenAI GPT**
- 🖥️ Clean, interactive UI built with **Streamlit**

---

## Architecture & Workflow

The diagram below shows the end-to-end sequence — from a user uploading a PDF to receiving a grounded answer.

```
┌─────────────┐
│  User (UI)  │
└──────┬──────┘
       │  1. Upload PDF(s)
       ▼
┌─────────────────────┐
│   Streamlit UI      │  ← app.py entry point
│  (sidebar uploader) │
└──────┬──────────────┘
       │  2. Read bytes
       ▼
┌─────────────────────┐
│     pdfplumber      │  ← extracts plain text page-by-page
└──────┬──────────────┘
       │  3. Raw text
       ▼
┌──────────────────────────────┐
│  RecursiveCharacterSplitter  │  ← splits into 1000-char chunks
│  (chunk_size=1000, overlap=200) │    with 200-char overlap
└──────┬───────────────────────┘
       │  4. List[str] chunks
       ▼
┌─────────────────────┐
│  OpenAI Embeddings  │  ← converts each chunk to a vector
└──────┬──────────────┘
       │  5. List[float] vectors
       ▼
┌─────────────────────┐
│   FAISS Vector DB   │  ← stores & indexes all vectors
└──────┬──────────────┘
       │  (index ready — stored in session state)
       │
       │  6. User types a question
       ▼
┌─────────────────────┐
│  Similarity Search  │  ← top-4 most relevant chunks retrieved
│  (FAISS retriever)  │
└──────┬──────────────┘
       │  7. Retrieved context chunks
       ▼
┌──────────────────────────────────┐
│  ChatPromptTemplate (LCEL chain) │  ← system prompt + chat_history
│  + chat history injection        │     + user question
└──────┬───────────────────────────┘
       │  8. Formatted prompt
       ▼
┌─────────────────────┐
│  ChatOpenAI (GPT)   │  ← generates grounded answer
└──────┬──────────────┘
       │  9. Answer text
       ▼
┌─────────────────────┐
│   Streamlit UI      │  ← renders answer in chat bubble
│  (chat messages)    │
└─────────────────────┘
```

---

## Key Concepts Used (Beginner-Friendly)

| # | Concept | What it means in this project |
|---|---------|-------------------------------|
| 1 | **Large Language Model (LLM)** | GPT-3.5-turbo reads context + question and writes a human-like answer |
| 2 | **Embeddings** | Numbers (vectors) that represent the *meaning* of text so similar ideas end up near each other in space |
| 3 | **Vector Store / Index** | A fast database (FAISS) that stores embeddings and finds the most similar ones to a query in milliseconds |
| 4 | **Retrieval-Augmented Generation (RAG)** | Instead of relying on the LLM's training data alone, we *retrieve* relevant chunks from the PDF and *augment* the prompt with them before *generating* an answer |
| 5 | **Text Chunking** | Long documents are split into smaller pieces so embeddings stay focused and retrieval stays precise |
| 6 | **LCEL (LangChain Expression Language)** | A pipe-based syntax (`chain = step1 \| step2 \| step3`) for composing LangChain components into a runnable pipeline |
| 7 | **Session State** | Streamlit re-runs the entire script on every interaction; `st.session_state` is the dictionary that persists objects (like the vector store) between re-runs |
| 8 | **Environment Variables** | Secrets (e.g. the OpenAI API key) are kept out of source code in a `.env` file and loaded at runtime with `python-dotenv` |
| 9 | **Prompt Engineering** | Crafting the system message that instructs the model to answer *only* from the provided context, reducing hallucinations |
| 10 | **Conversational Memory** | Past `HumanMessage`/`AIMessage` pairs are passed to the chain on every turn so the model maintains context across the conversation |

---

## Python vs C# — Concept Comparison

| Concept | Python (this project) | C# equivalent |
|---|---|---|
| **Package manager** | `pip install -r requirements.txt` | `dotnet restore` / NuGet |
| **Virtual environment** | `python -m venv .venv` | SDK-level isolation; `dotnet new` per project |
| **Environment variables** | `python-dotenv` loads `.env` → `os.getenv()` | `Microsoft.Extensions.Configuration` + `appsettings.json` / user-secrets |
| **HTTP / API client** | `openai` Python SDK (`ChatOpenAI`) | `Azure.AI.OpenAI` NuGet package or `HttpClient` |
| **Vector store** | `faiss-cpu` (in-process) | `Microsoft.SemanticKernel.Memory` or `Azure AI Search` |
| **LLM orchestration** | LangChain LCEL (`chain = A \| B \| C`) | Semantic Kernel `KernelFunction` pipeline |
| **PDF parsing** | `pdfplumber` | `iTextSharp` / `PdfPig` NuGet |
| **Web UI** | `streamlit run app.py` | Blazor / ASP.NET Core Razor Pages |
| **Session state** | `st.session_state` dictionary | `IHttpContextAccessor` session or Blazor `CascadingValue` |
| **Type hints** | `def foo(x: str) -> int:` | Native strong typing: `int Foo(string x)` |
| **Async** | `async def` / `await` | `async Task` / `await` |
| **List comprehension** | `[chunk for chunk in docs]` | LINQ: `docs.Select(chunk => chunk)` |

---

## Prerequisites

- Python 3.9 or higher
- An [OpenAI API key](https://platform.openai.com/account/api-keys)

---

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/nuthanm/chatbot-Q-A.git
   cd chatbot-Q-A
   ```

2. **Create and activate a virtual environment**

   > **Why a virtual environment?**
   > A virtual environment creates an isolated Python installation for this project.
   > This prevents dependency version conflicts between different projects on the same
   > machine — for example, if another project needs `openai==1.x` while this one
   > requires `openai==2.x`. It also keeps your global Python installation clean.

   ```bash
   # Create the virtual environment inside a folder called .venv
   python -m venv .venv
   ```

   ```bash
   # Activate on Windows (Command Prompt / PowerShell)
   .venv\Scripts\activate
   ```

   ```bash
   # Activate on macOS / Linux
   source .venv/bin/activate
   ```

   > Once activated, your terminal prompt will show `(.venv)` — all `pip install`
   > commands will now install packages only into this isolated environment.

3. **Install dependencies**

   ```bash
   # Install all pinned packages listed in requirements.txt
   pip install -r requirements.txt
   ```

4. **Configure your OpenAI API key**

   ```bash
   # Copy the template — never commit the real .env file
   cp .env.example .env
   ```

   Open `.env` in any editor and replace the placeholder with your actual key:

   ```
   OPENAI_API_KEY=sk-...
   ```

---

## Running the App

```bash
# Streamlit starts a local web server and opens the app in your browser
streamlit run app.py
```

The app will open automatically in your default browser at `http://localhost:8501`.

---

## How to Use

1. **Upload PDFs** – Use the sidebar to upload one or more PDF files.
2. **Process** – Click **Process PDFs** to extract text and build the search index.
3. **Ask questions** – Type your question in the chat input at the bottom of the page.
4. **Clear chat** – Use the **Clear Chat** button in the sidebar to reset the conversation.

---

## Tech Stack

| Library | Version | Official Docs | Purpose |
|---|---|---|---|
| [Streamlit](https://streamlit.io/) | 1.52.2 | [docs.streamlit.io](https://docs.streamlit.io) | Web UI |
| [pdfplumber](https://github.com/jsvine/pdfplumber) | 0.11.8 | [github.com/jsvine/pdfplumber](https://github.com/jsvine/pdfplumber) | PDF text extraction |
| [LangChain](https://www.langchain.com/) | 1.2.0 | [python.langchain.com](https://python.langchain.com/docs/introduction/) | LLM orchestration |
| [langchain-openai](https://pypi.org/project/langchain-openai/) | 1.1.6 | [api.python.langchain.com](https://api.python.langchain.com/en/latest/langchain_openai.html) | OpenAI LLM & embeddings |
| [langchain-community](https://pypi.org/project/langchain-community/) | 0.4.1 | [python.langchain.com/docs/integrations](https://python.langchain.com/docs/integrations/providers/) | FAISS vector store integration |
| [langchain-core](https://pypi.org/project/langchain-core/) | 1.2.5 | [api.python.langchain.com](https://api.python.langchain.com/en/latest/core_api_reference.html) | Core LangChain interfaces (LCEL) |
| [langchain-text-splitters](https://pypi.org/project/langchain-text-splitters/) | 1.1.0 | [python.langchain.com/docs/concepts/text_splitters](https://python.langchain.com/docs/concepts/text_splitters/) | Document chunking |
| [OpenAI Python SDK](https://github.com/openai/openai-python) | 2.14.0 | [platform.openai.com/docs](https://platform.openai.com/docs/introduction) | OpenAI API client |
| [faiss-cpu](https://github.com/facebookresearch/faiss) | 1.13.2 | [faiss.ai](https://faiss.ai/) | Vector similarity search |
| [tiktoken](https://github.com/openai/tiktoken) | 0.12.0 | [github.com/openai/tiktoken](https://github.com/openai/tiktoken) | Token counting |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | 1.0.1 | [saurabh-kumar.com/python-dotenv](https://saurabh-kumar.com/python-dotenv/) | Load `.env` secrets |

---

## Learning Resource

This project was built following concepts taught in the course:

> 🎓 **[Generative AI for Beginners](https://deloittedevelopment.udemy.com/course/generative-ai-for-beginners-b/learn/)** — Udemy
