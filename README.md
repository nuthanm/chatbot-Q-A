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

```mermaid
flowchart LR
    A(["👤 User"])
    B["🖥️ Streamlit UI\n(sidebar uploader)"]
    C["📄 pdfplumber\n(text extraction)"]
    D["✂️ RecursiveCharacter\nTextSplitter\nchunk=1000 / overlap=200"]
    E["🔢 OpenAI\nEmbeddings"]
    F[("🗄️ FAISS\nVector DB")]
    G(["❓ User Question"])
    H["🔍 Similarity\nSearch\ntop-4 chunks"]
    I["📝 LCEL Chain\nChatPromptTemplate\n+ chat_history"]
    J["🤖 ChatOpenAI\ngpt-3.5-turbo"]
    K["💬 Streamlit\nChat Bubble"]

    A -->|"① Upload PDF"| B
    B -->|"② Read bytes"| C
    C -->|"③ Raw text"| D
    D -->|"④ Chunks"| E
    E -->|"⑤ Vectors"| F

    G -->|"⑥ Embed question"| H
    F -->|"Index"| H
    H -->|"⑦ Context chunks"| I
    G -->|"⑦ Question"| I
    I -->|"⑧ Formatted prompt"| J
    J -->|"⑨ Answer"| K
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

Each section below explains **what the concept is**, **when to use it**, and shows **side-by-side code** for Python (used in this project) and the C# equivalent.

---

### 1. Package Manager

**What it is:** A tool that downloads, installs, and manages third-party libraries your code depends on.  
**When to use it:** Every time you want to add a new library or reproduce a project's environment from a list of dependencies.

**Python**
```python
# Install all dependencies from a lock file
pip install -r requirements.txt

# requirements.txt
langchain==1.2.0
openai==2.14.0
streamlit==1.52.2
```

**C#**
```csharp
// Restore all NuGet packages defined in the .csproj file
dotnet restore

// ChatBot.csproj
<PackageReference Include="Azure.AI.OpenAI" Version="1.0.0" />
<PackageReference Include="Microsoft.SemanticKernel" Version="1.0.0" />
```

---

### 2. Virtual Environment

**What it is:** An isolated Python installation that is scoped to a single project, keeping its packages separate from every other project on the machine.  
**When to use it:** Always — before installing any project dependencies, so different projects can use different library versions without conflicts.

**Python**
```bash
# Create the isolated environment
python -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Now pip installs go only into .venv/
pip install langchain
```

**C#**
```bash
# Each .NET project is already isolated by its .csproj file.
# No separate activation step is needed.
dotnet new console -n MyApp
cd MyApp
dotnet add package Azure.AI.OpenAI   # installs into this project only
```

---

### 3. Environment Variables / Secrets

**What it is:** Key-value pairs that live outside source code and carry sensitive configuration (API keys, connection strings).  
**When to use it:** Whenever your code needs secrets — never hard-code credentials in source files.

**Python**
```python
# .env file (never commit this)
OPENAI_API_KEY=sk-abc123

# app.py
from dotenv import load_dotenv
import os

load_dotenv()                          # reads .env into os.environ
api_key = os.getenv("OPENAI_API_KEY") # safely retrieve the value
```

**C#**
```csharp
// appsettings.json (or use dotnet user-secrets for local dev)
{
  "OpenAI": { "ApiKey": "sk-abc123" }
}

// Program.cs
using Microsoft.Extensions.Configuration;

var config = new ConfigurationBuilder()
    .AddJsonFile("appsettings.json")
    .AddEnvironmentVariables()          // overrides with real env vars in prod
    .Build();

string apiKey = config["OpenAI:ApiKey"]!;
```

---

### 4. HTTP / LLM API Client

**What it is:** A library that handles authentication, serialisation, and HTTP communication with the OpenAI (or Azure OpenAI) REST API.  
**When to use it:** When you need to send prompts to a language model and receive generated text back.

**Python**
```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
response = llm.invoke([HumanMessage(content="What is RAG?")])
print(response.content)
```

**C#**
```csharp
using Azure.AI.OpenAI;

var client = new OpenAIClient("sk-abc123");
var options = new ChatCompletionsOptions
{
    DeploymentName = "gpt-3.5-turbo",
    Messages = { new ChatRequestUserMessage("What is RAG?") }
};
ChatCompletions result = await client.GetChatCompletionsAsync(options);
Console.WriteLine(result.Choices[0].Message.Content);
```

---

### 5. Vector Store

**What it is:** A specialised database that stores embedding vectors and supports lightning-fast nearest-neighbour (similarity) search.  
**When to use it:** In RAG pipelines — store document chunks as vectors, then retrieve the most relevant chunks for a given query.

**Python**
```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
# Build index from a list of text chunks
vector_store = FAISS.from_texts(chunks, embedding=embeddings)

# Retrieve top-4 most similar chunks
retriever = vector_store.as_retriever(search_kwargs={"k": 4})
docs = retriever.invoke("What is the refund policy?")
```

**C#**
```csharp
using Microsoft.SemanticKernel.Memory;
using Microsoft.SemanticKernel.Connectors.AI.OpenAI;

var memory = new SemanticTextMemory(
    new VolatileMemoryStore(),                        // in-memory (like FAISS)
    new OpenAITextEmbeddingGenerationService("text-embedding-ada-002", "sk-abc123")
);

// Save a chunk
await memory.SaveInformationAsync("myCollection", id: "chunk1",
    text: "The refund policy allows returns within 30 days.");

// Search
await foreach (var result in memory.SearchAsync("myCollection",
    "What is the refund policy?", limit: 4))
    Console.WriteLine(result.Metadata.Text);
```

---

### 6. LLM Orchestration / Pipeline

**What it is:** A framework that chains together retrieval, prompt formatting, LLM calls, and output parsing into a single reusable pipeline.  
**When to use it:** When building multi-step AI workflows where the output of one step feeds into the next.

**Python (LCEL)**
```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

chain = (
    RunnablePassthrough.assign(
        context=lambda x: retriever.invoke(x["question"])
    )
    | prompt       # ChatPromptTemplate
    | llm          # ChatOpenAI
    | StrOutputParser()
)

answer = chain.invoke({"question": "What is RAG?", "chat_history": []})
```

**C# (Semantic Kernel)**
```csharp
using Microsoft.SemanticKernel;

var kernel = Kernel.CreateBuilder()
    .AddOpenAIChatCompletion("gpt-3.5-turbo", "sk-abc123")
    .Build();

// Define a prompt function
var fn = kernel.CreateFunctionFromPrompt(
    "Answer using this context: {{$context}}\n\nQuestion: {{$question}}");

var result = await kernel.InvokeAsync(fn, new KernelArguments
{
    ["context"] = retrievedChunks,
    ["question"] = "What is RAG?"
});
Console.WriteLine(result);
```

---

### 7. Web UI / App Framework

**What it is:** A framework that turns Python/C# code into an interactive web application with minimal boilerplate.  
**When to use it:** For data apps, internal tools, or demos where you want a working UI without writing HTML/CSS/JS.

**Python**
```python
import streamlit as st

st.title("PDF Q&A Chatbot")

# File uploader widget
uploaded = st.sidebar.file_uploader("Upload PDF", type="pdf",
                                     accept_multiple_files=True)
# Chat input
if question := st.chat_input("Ask a question..."):
    with st.chat_message("user"):
        st.write(question)
```

**C# (Blazor)**
```razor
@* Pages/Chat.razor *@
@page "/chat"

<h1>PDF Q&A Chatbot</h1>

<InputFile OnChange="HandleFile" />

@if (!string.IsNullOrEmpty(answer))
{
    <div class="chat-bubble">@answer</div>
}

@code {
    private string answer = "";

    private async Task HandleFile(InputFileChangeEventArgs e)
    {
        // process uploaded file
    }
}
```

---

### 8. Session / Application State

**What it is:** A mechanism to persist data (objects, lists, flags) across multiple user interactions within the same browser session.  
**When to use it:** To avoid re-building expensive objects (like a vector index) on every user action.

**Python**
```python
import streamlit as st

# First run: build the index and cache it
if "vector_store" not in st.session_state:
    st.session_state.vector_store = build_faiss_index(chunks)

# Subsequent runs: reuse the cached index
retriever = st.session_state.vector_store.as_retriever()
```

**C# (Blazor)**
```csharp
// Inject a scoped service — lives for the duration of the Blazor circuit (session)
@inject AppState State

@code {
    protected override async Task OnInitializedAsync()
    {
        if (State.VectorStore is null)
            State.VectorStore = await BuildFaissIndexAsync(chunks);
    }
}

// AppState.cs
public class AppState
{
    public IVectorStore? VectorStore { get; set; }
}
```

---

### 9. Type System

**What it is:** How the language communicates the expected data type of variables, parameters, and return values.  
**When to use it:** Always — type hints (Python) and static types (C#) catch bugs at development time and improve IDE support.

**Python**
```python
from typing import List
from langchain_core.messages import BaseMessage

def build_chain(chunks: List[str], history: List[BaseMessage]) -> str:
    """Returns the LLM answer as a plain string."""
    ...
```

**C#**
```csharp
using System.Collections.Generic;

// Types are mandatory — no hints needed, they're enforced by the compiler
string BuildChain(List<string> chunks, List<ChatMessage> history)
{
    // ...
    return answer;
}
```

---

### 10. Async / Non-blocking I/O

**What it is:** A concurrency model that allows the program to continue doing other work while waiting for slow operations (network calls, file I/O) to complete.  
**When to use it:** Whenever calling external APIs (OpenAI, databases) so the server doesn't block while waiting for a response.

**Python**
```python
import asyncio
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

async def get_answer(question: str) -> str:
    response = await llm.ainvoke([HumanMessage(content=question)])
    return response.content

asyncio.run(get_answer("What is embeddings?"))
```

**C#**
```csharp
using Azure.AI.OpenAI;

async Task<string> GetAnswerAsync(string question)
{
    var options = new ChatCompletionsOptions
    {
        Messages = { new ChatRequestUserMessage(question) }
    };
    var response = await client.GetChatCompletionsAsync(options); // non-blocking
    return response.Value.Choices[0].Message.Content;
}
```

---

### 11. List / Collection Processing

**What it is:** Concise ways to transform, filter, and aggregate collections of items.  
**When to use it:** When processing lists of document chunks, messages, or search results.

**Python**
```python
chunks = ["Hello world", "", "RAG is great", "  "]

# List comprehension — filter out empty/blank chunks
clean_chunks = [c for c in chunks if c.strip()]
# Result: ["Hello world", "RAG is great"]

# Map with a lambda
lengths = list(map(lambda c: len(c), clean_chunks))
# Result: [11, 12]
```

**C#**
```csharp
using System.Linq;

var chunks = new[] { "Hello world", "", "RAG is great", "  " };

// LINQ — filter out empty/blank chunks
var cleanChunks = chunks.Where(c => !string.IsNullOrWhiteSpace(c)).ToList();
// Result: ["Hello world", "RAG is great"]

// Select (map)
var lengths = cleanChunks.Select(c => c.Length).ToList();
// Result: [11, 12]
```

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
