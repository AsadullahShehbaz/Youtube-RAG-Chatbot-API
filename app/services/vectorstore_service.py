"""
Service for creating and managing vector stores.
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from app.core.config import settings


class VectorStoreService:
    """Handles text chunking, embedding, and vector store creation."""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
    
    def create_vectorstore(self, text: str) -> FAISS:
        """
        Create a FAISS vector store from text.
        
        Args:
            text: Raw text to be chunked and embedded
        
        Returns:
            FAISS vector store
        """
        # Split text into chunks
        chunks = self.text_splitter.create_documents([text])
        
        # Create vector store from chunks
        vectorstore = FAISS.from_documents(chunks, self.embedding_model)
        
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
        
        # Use similarity_search directly instead of retriever
        # This avoids the len() issue with FAISS
        retrieved_docs = vectorstore.similarity_search(query, k=k)
        
        return retrieved_docs