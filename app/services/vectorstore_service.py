"""
Service for creating and managing vector stores using FastEmbed + FAISS.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS
from fastembed import TextEmbedding
from app.core.config import settings
from app.core.logging_config import logger


class FastEmbedEmbeddings(Embeddings):
    """LangChain-compatible wrapper for FastEmbed."""

    def __init__(self, model_name: str = "BAAI/bge-small-en"):
        logger.debug(f"Initializing FastEmbedEmbeddings with model='{model_name}'")
        self.model = TextEmbedding(model_name=model_name)

    def embed_documents(self, texts):
        logger.info(f"Embedding {len(texts)} documents")
        # FastEmbed returns a generator, so convert to list
        embeddings = list(self.model.embed(texts))
        logger.debug(f"Generated embeddings for {len(embeddings)} documents")
        return embeddings

    def embed_query(self, text):
        logger.info(f"Embedding query: '{text[:50]}...' (truncated for log)")
        embedding = list(self.model.embed([text]))[0]
        logger.debug("Query embedding generated successfully")
        return embedding


class VectorStoreService:
    """Handles text chunking, embedding, and vector store creation."""

    def __init__(self):
        logger.debug("Initializing VectorStoreService...")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
        )
        logger.info(
            f"TextSplitter configured with chunk_size={settings.CHUNK_SIZE}, "
            f"chunk_overlap={settings.CHUNK_OVERLAP}"
        )
        self.embedding_model = FastEmbedEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
        logger.info(f"Embedding model set to '{settings.EMBEDDING_MODEL}'")

    def create_vectorstore(self, text: str) -> FAISS:
        """
        Create a FAISS vector store from text.

        Args:
            text: Raw text to be chunked and embedded

        Returns:
            FAISS vector store
        """
        logger.info("Creating vector store from input text")
        # Split text into chunks
        chunks = self.text_splitter.create_documents([text])
        logger.debug(f"Text split into {len(chunks)} chunks")

        # Create vector store from chunks
        vectorstore = FAISS.from_documents(chunks, self.embedding_model)
        logger.info("FAISS vector store created successfully")

        return vectorstore

    def retrieve_documents(self, vectorstore: FAISS, query: str, k: int = None):
        """
        Retrieve relevant documents from vector store.

        Args:
            vectorstore: FAISS vector store
            query: Search query
            k: Number of documents to retrieve

        Returns:
            List of relevant documents
        """
        if k is None:
            k = settings.RETRIEVER_K
        logger.info(f"Retrieving top {k} documents for query='{query}'")

        # Use similarity_search directly instead of retriever
        retrieved_docs = vectorstore.similarity_search(query, k=k)
        logger.debug(f"Retrieved {len(retrieved_docs)} documents from vector store")

        return retrieved_docs
