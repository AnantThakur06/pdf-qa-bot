from pypdf import PdfReader

reader = PdfReader("document.pdf")

text = ""

for page in reader.pages:
    text = text + page.extract_text()

print(len(text))