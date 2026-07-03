import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer, util

load_dotenv()

# --- Load and read the PDF ---
reader = PdfReader("document.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

# --- Chunk the text ---
chunk_size = 500
chunks = []
for i in range(0, len(text), chunk_size):
    chunks.append(text[i:i + chunk_size])

# --- Embed all chunks ---
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
chunk_embeddings = embed_model.encode(chunks)

# --- Function: question in, closest chunk out ---
def retrieve(question):
    question_embedding = embed_model.encode(question)
    scores = util.cos_sim(question_embedding, chunk_embeddings)[0]
    best_index = scores.argmax()
    return chunks[best_index]

# --- The LangChain pieces ---
model = ChatGroq(model="llama-3.3-70b-versatile")
prompt = ChatPromptTemplate.from_template(
    "Answer using ONLY this context.\n\nContext: {context}\n\nQuestion: {question}"
)
parser = StrOutputParser()

# --- The chain: context from retrieve(), question passed through ---
chain = (
    {"context": retrieve, "question": RunnablePassthrough()}
    | prompt
    | model
    | parser
)

# --- Run it: just pass the question ---
result = chain.invoke("What is Anant's favorite programming language?")

print(result)