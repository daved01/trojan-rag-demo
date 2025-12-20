import sys
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).parent.parent)) # Allows import of config when running from root

from chromadb import PersistentClient
from chromadb.api.models.Collection import Collection
from sentence_transformers import SentenceTransformer

import src.config as config


def load_documents() -> tuple[list[str], list[dict[str, Any]], list[str]]:
    """
    Reads all .txt files from the data directory.
    
    Returns:
        documents: list of text chunks.
        metadatas: list of metadata dicts (source file, chunk index).
        ids: list of unique IDs for the vector store.
    """

    documents: list[str] = []
    metadatas: list[dict[str, Any]] = []
    ids: list[str] = []
    
    print(f"Scanning directory: {config.DATA_DIR}")
    
    # Get all files
    files = list(config.DATA_DIR.glob("*.txt"))
    if not files:
        print("No text files found! Please add files to 'data/' folder.")
        return [], [], []

    for file_path in files:
        print(f"Processing: {file_path.name}")
        try:
            with open(file_path, "r", encoding="utf-8") as file_obj:
                text = file_obj.read()
        except Exception as error:
            print(f"Error reading {file_path.name}: {error}")
            continue
            
        # Simple chunking strategy: Split by double newlines (paragraphs)
        chunks = text.split("\n\n")
        
        for i, chunk in enumerate(chunks):
            clean_chunk = chunk.strip()
            # Skip empty or very short or empty lines
            if len(clean_chunk) < 20: 
                continue
                
            documents.append(clean_chunk)
            metadatas.append({"source": file_path.name, "chunk_index": i})
            ids.append(f"{file_path.name}_{i}")
            
    print(f"Processed {len(documents)} chunks from {len(files)} files.")
    return documents, metadatas, ids


def get_or_create_collection() -> Collection:
    """
    Sets up the ChromaDB client and creates a fresh collection.
    Deletes an existing collection.
    """

    print(f"Initializing ChromaDB at {config.DB_DIR}...")
    
    client = PersistentClient(path=str(config.DB_DIR))
    
    # Delete existing collection to ensure a clean state
    try:
        client.delete_collection(config.COLLECTION_NAME)
        print(f"Deleted old collection: {config.COLLECTION_NAME}")
    except Exception:
        pass  # Collection didn't exist
        
    collection = client.create_collection(name=config.COLLECTION_NAME)
    return collection


def ingest_data() -> None:
    """
    Main function to ingest data.
    """
    
    print("Starting ingestion ...")
    # Load data
    docs, metas, ids = load_documents()
    if not docs:
        print("Aborting ingestion: No documents found.")
        return

    embedding_model = SentenceTransformer(config.EMBEDDING_MODEL_NAME)
    
    # Generate embeddings
    print("Generating embeddings ...")
    embeddings = embedding_model.encode(docs).tolist()
    
    # Store in vector DB
    collection = get_or_create_collection()
    print("Indexing documents...")
    collection.add(
        documents=docs,
        embeddings=embeddings,
        metadatas=metas,
        ids=ids
    )
    
    print(f"Ingestion complete! {len(docs)} chunks stored successfully.")

if __name__ == "__main__":
    ingest_data()
