text = "abcdefghijklmnopqrstuvwxyz"

chunk_size = 5
chunks = []

print(f"Original text : {text}")
print(f"Length        : {len(text)}")
print("-" * 50)

for i in range(0, len(text), chunk_size):
    print(f"Current i = {i}")

    chunk = text[i:i + chunk_size]

    print(f"text[{i}:{i + chunk_size}] -> '{chunk}'")

    chunks.append(chunk)

    print(f"Chunks so far: {chunks}")
    print("-" * 50)

print("\nFinal Result")
print(chunks)