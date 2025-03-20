import aiohttp
import asyncio
from bs4 import BeautifulSoup
from app.utils.logging import logger
from playwright.async_api import async_playwright
from langchain_core.documents import Document
from datetime import datetime
from typing import List

class CompanyWebScraper:

    async def clean_text(self, text):
        """Clean extracted text by removing extra whitespace and normalizing"""
        import re
        # Remove special characters but keep basic punctuation 
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text.strip()

    async def scrape_content(self, urls: List[str] | str, max_concurrent=100):
        """
        Scrape content from multiple URLs concurrently using BeautifulSoup first,
        falling back to Playwright if needed
        """

        if isinstance(urls, str):
            urls = [urls]

        results = []
        
        async def process_url(url, session):
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            try:
                # First try with aiohttp
                async with session.get(url, headers=headers) as response:     
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, "html.parser")
                        
                        # Extract text
                        text = ' \n'.join(soup.stripped_strings)
                        clean_content = await self.clean_text(text)
                        return Document(
                            page_content=clean_content,
                            metadata={"source": url, "timestamp": datetime.now().isoformat()}
                        )
                    else:
                        # Fall back to Playwright
                        async with async_playwright() as p:
                            browser = await p.chromium.launch(headless=True)
                            page = await browser.new_page()
                            
                            await page.goto(url)
                            await page.wait_for_load_state("networkidle")
                            
                            html = await page.content()
                            soup = BeautifulSoup(html, "html.parser")
                            
                            text = ' \n'.join(soup.stripped_strings)
                            clean_content = await self.clean_text(text)
                            
                            await browser.close()
                            return Document(
                                page_content=clean_content,
                                metadata={"source": url, "timestamp": datetime.now().isoformat()}
                            )            
            except Exception as e:
                logger.error(f"Both methods failed for {url}")
                return Document(
                    page_content="No content found",
                    metadata={"source": url, "timestamp": datetime.now().isoformat()}
                )     

        async with aiohttp.ClientSession() as session:
            for i in range(0, len(urls), max_concurrent):
                chunk = urls[i:i + max_concurrent]
                chunk_tasks = [process_url(url, session) for url in chunk]
                chunk_results = await asyncio.gather(*chunk_tasks)
                results.extend(chunk_results)
                
        return results
