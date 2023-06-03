"""Load html from files, clean up, split, ingest into Weaviate."""
import os
import pickle
from typing import List

from langchain.docstore.document import Document
from langchain.document_loaders import TextLoader, PyPDFLoader, CSVLoader, ObsidianLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS

from constant import SOURCE_DIRECTORY

def load_single_document(file_path: str) -> List[Document]:
    # Loads a single document from a file path
    if file_path.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf8")
    elif file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".csv"):
        loader = CSVLoader(file_path)
    elif file_path.endswith(".obs"):
        f = open(file_path, 'r')
        obsidian_path = f.readline()
        print(obsidian_path)
        loader = ObsidianLoader(obsidian_path.strip())
    docs = loader.load()
    print(f"Loaded {len(docs)} documents from {file_path}")
    return docs


def load_documents(source_dir: str) -> List[Document]:
    # Loads all documents from source documents directory
    all_files = os.listdir(source_dir)
    docs = []
    for file_path in all_files  :
        if file_path[-4:] in ['.txt', '.pdf', '.csv', '.obs']:
            absolute_path = (f"{source_dir}/{file_path}") 
            docs += load_single_document(absolute_path)

    return docs


def ingest_docs():
    """Get documents from web pages."""

    print(f"Loading documents from {SOURCE_DIRECTORY}")
    documents = load_documents(SOURCE_DIRECTORY)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    print(f"Loaded {len(documents)} documents from {SOURCE_DIRECTORY}")
    print(f"Split into {len(texts)} chunks of text")

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(texts, embeddings)

    # Save vectorstore
    with open("vectorstore.pkl", "wb") as f:
        pickle.dump(vectorstore, f)

if __name__ == "__main__":
    ingest_docs()
