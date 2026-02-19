from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

class SentenceTransformerWrapper:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        return self.model.encode(texts, convert_to_tensor=True).tolist()

    def embed_query(self, text):
        return self.model.encode([text], convert_to_tensor=True)[0].tolist()

DATA_PATH = "data"
DB_PATH = "data/faiss_index"

def main():
    docs = []
    for file in os.listdir(DATA_PATH):
        if file.endswith(".txt"):
            filepath = os.path.join(DATA_PATH, file)
            with open(filepath, "r") as f:
                text = f.read()

            # Split by section dividers (---) for files that contain multiple entries
            sections = [s.strip() for s in text.split("---") if s.strip()]

            for section in sections:
                docs.append(Document(
                    page_content=section,
                    metadata={"source": file}
                ))

    # Further split large sections into smaller chunks for better retrieval
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " "]
    )
    split_docs = splitter.split_documents(docs)

    print(f"📄 Loaded {len(docs)} sections from {len(set(d.metadata['source'] for d in docs))} files")
    print(f"✂️  Split into {len(split_docs)} chunks for indexing")

    # Local embedding model (no API quota issues)
    embedder = SentenceTransformerWrapper("sentence-transformers/all-MiniLM-L6-v2")

    texts = [d.page_content for d in split_docs]
    metadatas = [d.metadata for d in split_docs]

    faiss_store = FAISS.from_texts(texts, embedder, metadatas=metadatas)
    faiss_store.save_local(DB_PATH)

    print(f"✅ Ingestion complete! {len(split_docs)} chunks indexed into FAISS at '{DB_PATH}'")

if __name__ == "__main__":
    main()
