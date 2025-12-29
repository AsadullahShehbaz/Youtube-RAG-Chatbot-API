"""
Service for LLM interaction and answer generation.
"""
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
from langchain_groq import ChatGroq
from app.core.logging_config import logger


class LLMService:
    """Handles LLM-based question answering."""
    
    def __init__(self):
        logger.debug("Initializing LLMService...")
        self.llm = ChatGroq(
            model=settings.LLM_MODEL,
            api_key=settings.GROQ_API_KEY
        )
        logger.info(f"LLM initialized with model='{settings.LLM_MODEL}'")

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
        logger.debug("Prompt template configured")

        self.parser = StrOutputParser()
        logger.debug("Output parser initialized")
    
    def format_documents(self, documents) -> str:
        """
        Format retrieved documents into a single context string.
        
        Args:
            documents: List of retrieved documents
        
        Returns:
            Formatted context string
        """
        logger.info(f"Formatting {len(documents)} retrieved documents into context string")
        formatted_context = "\n\n".join(doc.page_content for doc in documents)
        logger.debug(f"Formatted context length={len(formatted_context)} characters")
        return formatted_context
    
    def generate_answer(self, context: str, question: str) -> str:
        """
        Generate an answer using the LLM.
        
        Args:
            context: Context text from retrieved documents
            question: User's question
        
        Returns:
            Generated answer
        """
        logger.info(f"Generating answer for question='{question}'")
        
        # Create prompt with context and question
        final_prompt = self.prompt_template.invoke({
            'context': context,
            'question': question
        })
        logger.debug("Prompt constructed and passed to LLM")

        try:
            # Generate answer from LLM
            response = self.llm.invoke(final_prompt)
            logger.info("LLM response received successfully")
            logger.debug(f"Raw LLM response length={len(response.content)} characters")
            
            # Parse and return answer content
            return response.content
        except Exception as e:
            logger.error(f"Error during LLM answer generation: {e}", exc_info=True)
            raise
