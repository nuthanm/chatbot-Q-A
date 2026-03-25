# chatbot-Q-A

Upload your PDF documents and get instant answers using our AI-powered chatbot.

## Features

- 📄 Upload one or more PDF files
- 🔍 Intelligent text extraction using **pdfplumber**
- 🧠 Semantic search powered by **FAISS** vector store and **OpenAI Embeddings**
- 💬 Conversational Q&A with chat history via **LangChain** + **OpenAI GPT**
- 🖥️ Clean, interactive UI built with **Streamlit**

## Prerequisites

- Python 3.9 or higher
- An [OpenAI API key](https://platform.openai.com/account/api-keys)

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/nuthanm/chatbot-Q-A.git
   cd chatbot-Q-A
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your OpenAI API key**

   Copy the example environment file and add your key:

   ```bash
   cp .env.example .env
   ```

   Open `.env` and replace `your_openai_api_key_here` with your actual key:

   ```
   OPENAI_API_KEY=sk-...
   ```

## Running the App

```bash
streamlit run app.py
```

The app will open automatically in your default browser at `http://localhost:8501`.

## How to Use

1. **Upload PDFs** – Use the sidebar to upload one or more PDF files.
2. **Process** – Click **Process PDFs** to extract text and build the search index.
3. **Ask questions** – Type your question in the chat input at the bottom of the page.
4. **Clear chat** – Use the **Clear Chat** button in the sidebar to reset the conversation.

## Tech Stack

| Library | Version | Purpose |
|---|---|---|
| streamlit | 1.52.2 | Web UI |
| pdfplumber | 0.11.8 | PDF text extraction |
| langchain | 1.2.0 | LLM orchestration |
| langchain-openai | 1.1.6 | OpenAI LLM & embeddings |
| langchain-community | 0.4.1 | FAISS vector store integration |
| langchain-core | 1.2.5 | Core LangChain interfaces |
| langchain-text-splitters | 1.1.0 | Document chunking |
| openai | 2.14.0 | OpenAI API client |
| faiss-cpu | 1.13.2 | Vector similarity search |
| tiktoken | 0.12.0 | Token counting |
