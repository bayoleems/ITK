import os
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from app.models.web_search import WebSearchResult
from app.models.semantic_search import SemanticSearch

class LLMService:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
        self.web_search_parser = PydanticOutputParser(pydantic_object=WebSearchResult)
        self.semantic_search_parser = PydanticOutputParser(pydantic_object=SemanticSearch)

    async def semantic_search_llm(self, vector_store, query: str) -> SemanticSearch:
        """
        Query the vector store for relevant documents and structure them using LLM
        """
        # Get relevant documents from vector store
        docs = vector_store.similarity_search(query, k=2)

        # Combine document contents 
        raw_text = ""

        for doc in docs:
            raw_text += f"Timestamp: {doc.metadata['timestamp']}\n"
            raw_text += f"Content: {doc.page_content}\n"
            raw_text += f"Source: {doc.metadata['source']}\n"
            raw_text += f"-----------------------------------\n"

        # Create prompt template
        prompt = ChatPromptTemplate.from_template(
            """
            You are a helpful assistant that summarizes chunks of text.
            Below is raw text. Please provide a comprehensive summary that may be related to the query.

            Raw text: {text}

            Make sure to include all relevant information from the raw text.
            
            Your response should match this exact format:
            
            {format_instructions}"""
        )
        
        # Create chain and run
        chain = prompt | self.model | self.semantic_search_parser
        structured_response = chain.invoke({
            "text": raw_text,
            "query": query,
            "format_instructions": self.semantic_search_parser.get_format_instructions()
        })
        
        return structured_response

    async def web_search_llm(self, query: str) -> WebSearchResult:
        """
        Perform web search and structure results using LLM
        """

        search = DuckDuckGoSearchRun()
        search_results = search.invoke(f"{query}")
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_template(
            """You are a helpful assistant that analyzes information.
            Below is the search results for a query. Please provide a comprehensive summary
            of the search results.
    
            Search results: {text}
            Query: {query}

            Focus on information that is most relevant to the query while maintaining accuracy.
            
            Your response should match this exact format:
            
            {format_instructions}"""
        )
        
        # Create chain and run
        chain = prompt | self.model | self.web_search_parser
        structured_response = chain.invoke({
            "text": search_results,
            "query": query,
            "format_instructions": self.web_search_parser.get_format_instructions()
        })

        
        return structured_response
