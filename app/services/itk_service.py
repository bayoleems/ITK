from abc import abstractmethod
import asyncio
from app.models.semantic_search import SemanticSearch
from app.models.web_search import WebSearchResult
from app.services.llm_service import LLMService
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import Document
from typing import List
from app.utils.logging import logger
from app.services.scrape_service import CompanyWebScraper
from app.services.vectorstore_service import VectorStoreService
import pandas as pd


class ITKService:
    def __init__(self):
        self.scrape_service = CompanyWebScraper()
        self.vector_store_service = VectorStoreService()
        self.llm_service = LLMService()

    async def chat(self, query: str, company_name: str = None):
        """
        Chat with ITK
        """
        if not company_name:
            company_name = await self.vector_store_service.get_or_create_vectorstore('all_companies')
        else:
            company_name = await self.vector_store_service.get_or_create_vectorstore(company_name)

        # Get web search and semantic search results
        web_search, semantic_search = await asyncio.gather(
            self.llm_service.web_search_llm(query),
            self.llm_service.semantic_search_llm(vector_store=company_name, query=query)
        )

        response = await self._itk_chat_chain(query, web_search, semantic_search)

        return response

    def load_data_from_csv(self, file_path: str):
        df = pd.read_csv(file_path)
        return df
    
    def parse_results(self, results: List[Document] , df: pd.DataFrame):
        """
        Parse the results from the scrape service and return a dictionary of company documents.
        """
        company_docs = {}
        company_results = list(map(lambda result: {
            f"{df[df['URL'] == result.metadata['source']]['Company'].iloc[0]}" : result},
              results))
        
        # Group documents by company
        
        for result_dict in company_results:
            for company, doc in result_dict.items():
                if company not in company_docs:
                    company_docs[company] = []
                company_docs[company].append(doc)

        return company_docs
    
    async def _itk_chat_chain(self, query: str, web_search: WebSearchResult, semantic_search: SemanticSearch):
        """
        Combine web search and semantic search results to provide a comprehensive response to the user's query
        """

        prompt = ChatPromptTemplate.from_template(
            """
            You are an intelligent assistant, I.T.K. (I Too Know), with access to regularly updated information about companies. 
            You have two sources of information:

            1. Recent web search results: {web_search}
            2. Information from our database: {semantic_search}
            
            Query: {query}

            Please provide a comprehensive and accurate response that:
            - Prioritizes the most recent and relevant information
            - Maintains factual accuracy and avoids speculation
            - Provides specific citations when possible
            - Focuses on directly answering the user's query
            - For company-specific queries, emphasizes information from our database first
            - For industry or multi-company queries, synthesizes information from both sources
            
            If you don't have enough information to fully answer the query, be transparent about what you do and don't know.


            Response:

            """
        )

        chain = prompt | self.llm_service.model

        response = await chain.ainvoke({
            "web_search": web_search.model_dump(),
            "semantic_search": semantic_search.model_dump(),
            "query": query
        })

        return response.content

    async def scrape_and_store_data(self, file_path: str):
        df = self.load_data_from_csv(file_path)

        # Scrape content for all URLs in the dataframe
        all_urls = df['URL'].tolist()
        results = await self.scrape_service.scrape_content(all_urls)

        # Parse the results
        company_docs = self.parse_results(results, df)

        # Store the results in the vector store
        tasks = []
        for company, docs in company_docs.items():
            task = self.vector_store_service.embed_documets(company, docs)
            tasks.append(task)

        await asyncio.gather(*tasks)

        logger.info(f"scraped and stored data for {len(results)} links")

    @abstractmethod
    def load_data_from_db(self):
        """Load data from database"""
        pass
    
    @abstractmethod
    def store_data_in_db(self, results: list):
        """Store data in database"""
        pass

    @abstractmethod
    def load_chat_history(self):
        """Load chat history"""
        pass
    
    @abstractmethod
    def store_chat_history(self, chat_history: list):
        """Store chat history"""
        pass

    