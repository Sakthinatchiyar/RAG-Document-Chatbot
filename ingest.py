
from pathlib import Path
import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "documents"
DB_DIR = BASE_DIR / "chroma_db"

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to local ChromaDB
client = chromadb.PersistentClient(path=str(DB_DIR))

# Create a fresh collection for ingestion
try:
    client.delete_collection("study_documents")
except Exception:
    pass

collection = client.get_or_create_collection(
    name="study_documents",
    metadata={"hnsw:space": "cosine"}
)

# Split text into overlapping token chunks
def split_into_chunks(text, chunk_size=500, overlap=80):
    tokens = model.tokenizer.encode(
        text,
        add_special_tokens=False
    )

    chunks = []
    step = chunk_size - overlap

    for start in range(0, len(tokens), step):
        chunk_tokens = tokens[start:start + chunk_size]

        if not chunk_tokens:
            continue

        chunk_text = model.tokenizer.decode(chunk_tokens)

        if chunk_text.strip():
            chunks.append(chunk_text)

    return chunks


all_chunks = []
all_metadata = []
all_ids = []

chunk_number = 0

# Read every PDF
pdf_files = list(DOCS_DIR.glob("*.pdf"))

if not pdf_files:
    raise ValueError("No PDF files found in documents folder!")

for pdf_file in pdf_files:
    print(f"Reading: {pdf_file.name}")

    reader = PdfReader(str(pdf_file))

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if not text.strip():
            continue

        page_chunks = split_into_chunks(text)

        for chunk in page_chunks:
            chunk_number += 1

            all_chunks.append(chunk)

            all_metadata.append({
                "source": pdf_file.name,
                "page": page_number
            })

            all_ids.append(f"chunk_{chunk_number}")

# Check extracted content
if not all_chunks:
    raise ValueError(
        "No text extracted. Check whether your PDFs contain selectable text."
    )

print("Generating embeddings...")

embeddings = model.encode(
    all_chunks,
    convert_to_numpy=True,
    show_progress_bar=True
).tolist()

# Store chunks and vectors in ChromaDB
collection.add(
    ids=all_ids,
    documents=all_chunks,
    embeddings=embeddings,
    metadatas=all_metadata
)

print("\nIngestion completed successfully!")
print("Total chunks:", collection.count())

# Display sample chunks
print("\nSample chunks:")

for i, chunk in enumerate(all_chunks[:3], start=1):
    print(f"\nCHUNK {i}:")
    print(chunk[:500])
