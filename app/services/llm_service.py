"""
Service for LLM interaction and answer generation.
"""
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
from langchain_groq import ChatGroq

class LLMService:
    """Handles LLM-based question answering."""
    
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.LLM_MODEL,
            api_key=settings.GROQ_API_KEY
        )
        
        self.prompt_template = PromptTemplate(
            template="""You are a helpful assistant.
Answer only from the provided context.
If the context is insufficient, just say "I don't know based on the video content."

Context:
{context}

Question: {question}

Answer:""",
            input_variables=['context', 'question']
        )
        
        self.parser = StrOutputParser()
    
    def format_documents(self, documents) -> str:
        """
        Format retrieved documents into a single context string.
        
        Args:
            documents: List of retrieved documents
        
        Returns:
            Formatted context string
        """
        print(f"Received {len(documents)} documents for formating")
        return "\n\n".join(doc.page_content for doc in documents)
    
    def generate_answer(self, context: str, question: str) -> str:
        """
        Generate an answer using the LLM.
        
        Args:
            context: Context text from retrieved documents
            question: User's question
        
        Returns:
            Generated answer
        """
        # Create prompt with context and question
        final_prompt = self.prompt_template.invoke({
            'context': context,
            'question': question
        })
        
        # Generate answer from LLM
        response = self.llm.invoke(final_prompt)
        
        print(f"Generated answer for question {question} : {response.content}")
        # Parse and return answer content
        return response.content