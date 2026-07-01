import os
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer, util

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Step 1: read the PDF
reader = PdfReader("document.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

# Step 2: chunk it
chunk_size = 500
chunks = []
for i in range(0, len(text), chunk_size):
    chunks.append(text[i:i + chunk_size])

# Step 3: embed all chunks ONCE (doesn't change between questions)
model = SentenceTransformer("all-MiniLM-L6-v2")
chunk_embeddings = model.encode(chunks)

print("PDF Q&A bot ready! Type 'quit' to exit.")

while True:
    question = input("\nYour question: ")

    if question.lower() == "quit":
        print("Goodbye!")
        break

    # Step 4: embed the question
    question_embedding = model.encode(question)

    # Step 5: find the closest chunk (RETRIEVAL)
    # scores = util.cos_sim(question_embedding, chunk_embeddings)
    # best_index = scores.argmax()
    # best_chunk = chunks[best_index]
    # Step 5: find the TOP 3 closest chunks (RETRIEVAL)
    scores = util.cos_sim(question_embedding, chunk_embeddings)[0]
    top_indices = scores.topk(3).indices

    best_chunks = ""
    for index in top_indices:
        best_chunks += f"{chunks[index]}\n\n"

    # Step 6: feed the chunk to the LLM (GENERATION)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"Answer using ONLY this text. If the answer isn't here, say you don't know. Text: {best_chunks}"},
            {"role": "user", "content": question}
        ]
    )

    answer = response.choices[0].message.content.strip()
    print("Answer:", answer)