from typing import List
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from utills.logging import logger
from dotenv import load_dotenv
load_dotenv()

class VectorStoreService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=750,chunk_overlap=50)
        self.embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"), model='text-embedding-3-small')
        # self.chroma_client = chromadb.HttpClient(host='localhost', port=8000)

    async def get_or_create_vectorstore(self, company: str):
        try:    
            langchain_chroma = Chroma(
                # client=self.chroma_client,
                collection_name=f'{company.strip().lower()}_vectorstore',
                embedding_function=self.embeddings,
                persist_directory=f'./chroma_db'
            )
            return langchain_chroma
        
        except Exception as e:
            logger.error(f"Error creating vectorstore: {str(e)}")
            raise

    async def embed_documets(self, company: str, docs: List[Document]) -> list:
        try:    
            vector_store = await self.get_or_create_vectorstore(company)
            text = self.text_splitter.split_documents(docs)
            await vector_store.aadd_documents(text)

            logger.info(f"web content successfully added to {company}")

            all_companies = await self.get_or_create_vectorstore('all_companies')
            await all_companies.aadd_documents(text)

        except Exception as e:
            logger.error(f"Error embedding documents: {str(e)}")
            raise
