import os
import subprocess
import json
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage, Document, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# ==========================
# Constants
# ==========================
BASE_INDEX_DIR = "index_storage"  # Where per-project indexes live
INCLUDE_EXTENSIONS = (".js", ".ts", ".jsx", ".tsx", ".vue", ".css", ".html", ".py")
EXCLUDE_PATTERNS = ["node_modules/", ".git/", "dist/", "build/", "__pycache__/"]
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
OLLAMA_MODEL = "llama3"  # Pick your Ollama model

os.makedirs(BASE_INDEX_DIR, exist_ok=True)
def get_index_dir(project_path: str) -> str:
    """Return the index folder for this project."""
    project_name = os.path.basename(os.path.abspath(project_path))
    return os.path.join(BASE_INDEX_DIR, project_name)


def _gather_project_files(project_path: str):
    """Recursively gather project files matching filters."""
    matched_files = []
    for root, dirs, files in os.walk(project_path):
        if any(pattern.rstrip("/") in root for pattern in EXCLUDE_PATTERNS):
            continue
        for file in files:
            if file.endswith(INCLUDE_EXTENSIONS):
                matched_files.append(os.path.join(root, file))
    return matched_files

CHUNK_SIZE = 500  # number of characters per chunk
CHUNK_OVERLAP = 50  # number of characters overlap between chunks


def _chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    text_length = len(text)
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def build_index(project_path: str):
    """Build a LlamaIndex vector index from project files using chunking."""
    embedding = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
    Settings.embed_model = embedding
    Settings.llm = None

    index_dir = get_index_dir(project_path)
    os.makedirs(index_dir, exist_ok=True)

    print(f"[INFO] Gathering project files from {project_path}...")
    files = _gather_project_files(project_path)
    if not files:
        print("[WARNING] No files matched for indexing.")
        return

    documents = []
    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Split into chunks
            chunks = _chunk_text(content)
            for i, chunk in enumerate(chunks):
                doc_id = f"{file_path}_chunk{i}"
                documents.append(Document(text=chunk, doc_id=doc_id))
        except Exception as e:
            print(f"[WARNING] Failed to read {file_path}: {e}")

    print(f"[INFO] Building vector index with {len(documents)} chunks...")
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=StorageContext.from_defaults()
    )

    index.storage_context.persist(persist_dir=index_dir)
    print(f"[INFO] Index saved to {index_dir}")


def query_index(project_path: str, query: str, top_k: int = 3) -> str:
    """Query the index and run the result through Ollama (unchanged output)."""
    embedding = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
    Settings.embed_model = embedding
    Settings.llm = None

    index_dir = get_index_dir(project_path)
    if not os.path.exists(index_dir) or not os.listdir(index_dir):
        raise ValueError(f"[ERROR] Index not found for project: {project_path}")

    storage_context = StorageContext.from_defaults(persist_dir=index_dir)
    index = load_index_from_storage(storage_context)

    query_engine = index.as_query_engine(similarity_top_k=top_k)
    response = query_engine.query(query)

    return response












