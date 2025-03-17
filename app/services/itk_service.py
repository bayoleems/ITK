from abc import abstractmethod
import asyncio
from utills.logging import logger
from app.services.scrape_service import CompanyWebScraper
from app.services.vectorstore_service import VectorStoreService
import pandas as pd

class ITKService:
    def __init__(self):
        self.scrape_service = CompanyWebScraper()
        self.vector_store_service = VectorStoreService()

    def load_data_from_csv(self, file_path: str):
        df = pd.read_csv(file_path)
        return df
    
    def parse_results(self, results: list, df: pd.DataFrame):
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
    
    @abstractmethod
    def load_data_from_db(self):
        """Load data from database"""
        pass

    @abstractmethod
    def store_data_in_db(self, results: list):
        """Store data in database"""
        pass

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


        logger.info(f"Scraped and stored data for {len(results)} companies")


