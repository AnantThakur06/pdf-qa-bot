from pypdf import PdfReader
from sentence_transformers import SentenceTransformer, util

# Step 1: read the PDF into text
reader = PdfReader("document.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

# Step 2: chunk the text into 500-character pieces
chunk_size = 500
chunks = []
for i in range(0, len(text), chunk_size):
    chunks.append(text[i:i + chunk_size])

# Step 3: load the model and embed all chunks
model = SentenceTransformer("all-MiniLM-L6-v2")
chunk_embeddings = model.encode(chunks)

# Step 4: take a question and embed it
question = "What is Anant's favorite programming language?"
question_embedding = model.encode(question)

# Step 5: find the closest chunk to the question
scores = util.cos_sim(question_embedding, chunk_embeddings)
best_index = scores.argmax()

print("Question:", question)
print("Best matching chunk number:", int(best_index))
print("--- The matching chunk text ---")
print(chunks[best_index])