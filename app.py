import pdfplumber
import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PDF Chatbot",
    page_icon="📄",
    layout="wide",
)

st.title("📄 PDF Q&A Chatbot")
st.markdown(
    "Upload one or more PDF documents and ask any questions about their content."
)

# ── Session-state defaults ────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history: list[HumanMessage | AIMessage] = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "processed_files" not in st.session_state:
    st.session_state.processed_files: list[str] = []


# ── Helpers ───────────────────────────────────────────────────────────────────
def extract_text_from_pdfs(uploaded_files) -> str:
    """Extract plain text from a list of uploaded PDF files."""
    combined_text = ""
    for uploaded_file in uploaded_files:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    combined_text += page_text + "\n"
    return combined_text


def build_vector_store(text: str) -> FAISS:
    """Split *text* into chunks, embed them, and return a FAISS vector store."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_text(text)
    if not chunks:
        raise ValueError(
            "The document text could not be split into processable chunks. "
            "Please check that the PDF contains enough readable content."
        )
    embeddings = OpenAIEmbeddings()
    return FAISS.from_texts(chunks, embeddings)


def build_rag_chain(vector_store: FAISS):
    """Build a conversational RAG chain using LCEL."""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Answer the user's question using only "
                "the context provided below. If the answer is not contained in the "
                "context, say so honestly.\n\nContext:\n{context}",
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        RunnablePassthrough.assign(
            context=lambda x: format_docs(retriever.invoke(x["question"]))
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


# ── Sidebar – PDF upload & processing ────────────────────────────────────────
with st.sidebar:
    st.header("📁 Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose PDF file(s)",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if st.button("Process PDFs", disabled=not uploaded_files):
        file_names = [f.name for f in uploaded_files]
        with st.spinner("Extracting text and building index…"):
            try:
                raw_text = extract_text_from_pdfs(uploaded_files)
                if not raw_text.strip():
                    st.error(
                        "No readable text found in the uploaded PDF(s). "
                        "Please ensure the files contain selectable text."
                    )
                else:
                    st.session_state.vector_store = build_vector_store(raw_text)
                    st.session_state.rag_chain = build_rag_chain(
                        st.session_state.vector_store
                    )
                    st.session_state.processed_files = file_names
                    st.session_state.chat_history = []
                    st.success(
                        f"✅ Processed {len(file_names)} file(s). "
                        "You can now ask questions!"
                    )
            except Exception as exc:
                st.error(f"Error processing PDFs: {exc}")

    if st.session_state.processed_files:
        st.markdown("**Loaded documents:**")
        for name in st.session_state.processed_files:
            st.markdown(f"- {name}")

    if st.button("🗑️ Clear Chat", disabled=not st.session_state.chat_history):
        st.session_state.chat_history = []
        st.rerun()

# ── Main area – chat interface ────────────────────────────────────────────────
if st.session_state.rag_chain is None:
    st.info("👈 Upload and process at least one PDF to get started.")
else:
    # Display existing chat history
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        else:
            with st.chat_message("assistant"):
                st.markdown(message.content)

    # Accept new user input
    user_question = st.chat_input("Ask a question about your document(s)…")
    if user_question:
        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                try:
                    answer = st.session_state.rag_chain.invoke(
                        {
                            "question": user_question,
                            "chat_history": st.session_state.chat_history,
                        }
                    )
                    st.markdown(answer)

                    st.session_state.chat_history.append(
                        HumanMessage(content=user_question)
                    )
                    st.session_state.chat_history.append(
                        AIMessage(content=answer)
                    )
                except Exception as exc:
                    error_msg = str(exc)
                    st.error(f"Error generating answer: {error_msg}")
