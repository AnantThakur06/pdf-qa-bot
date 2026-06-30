from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

text = "Python is my favorite programming language"
embedding = model.encode(text)

print("The text was:", text)
print("Number of values in the embedding:", len(embedding))
print("First 10 values:", embedding[:10])