from pypdf import PdfReader

# Step 1: read the PDF into text (you know this)
reader = PdfReader("document.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

# Step 2: chunk the text into pieces of 500 characters
chunk_size = 500
chunks = []

for i in range(0, len(text), chunk_size):
    chunk = text[i:i + chunk_size]
    chunks.append(chunk)


print(f"Total characters in document: {len(text)}")
print(f"Number of chunks created: {len(chunks)}")
# print("--- First chunk ---")
print(chunks[0])
for index, chunk in enumerate(chunks):
    print(f"--- Chunk {index} ---")
    print(chunk)
    print()