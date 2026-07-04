import os
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# --- Read the PDF ---
reader = PdfReader("document.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

# --- Split into chunks (smart splitter) ---
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_text(text)
print(f"Number of chunks: {len(chunks)}")

# --- Build the FAISS vector store ---
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.from_texts(chunks, embeddings)
print("Vector store built!")

# --- Search test (top 3 closest chunks) ---
results = vector_store.similarity_search("What is Anant's favorite programming language?", k=3)
print("--- Top matching chunks ---")
for doc in results:
    print(doc.page_content)
    print("---")

# --- Turn the vector store into a retriever ---
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# --- The LangChain pieces ---
model = ChatGroq(model="llama-3.3-70b-versatile")
prompt = ChatPromptTemplate.from_template(
    "Answer using ONLY this context.\n\nContext: {context}\n\nQuestion: {question}"
)
parser = StrOutputParser()

# --- The complete FAISS RAG chain ---
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | parser
)

# --- Run it ---
answer = chain.invoke("What is Anant's favorite programming language?")
print("\n=== ANSWER ===")
print(answer)