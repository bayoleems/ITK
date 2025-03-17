from datetime import datetime
import os
from langchain_community.utilities import ApifyWrapper
from langchain_core.document_loaders.base import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

def chunk_data(data, chunk_size=2000, chunk_overlap=200):
    """Split documents into chunks"""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(data)
    return docs

def semantic_search(query, db, k=4):
    """Search documents in ChromaDB"""
    results = db.similarity_search(query, k=k)
    return results

# Initialize embeddings
embeddings = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"], model="text-embedding-3-small")

# Initialize Apify client
apify = ApifyWrapper(apify_api_token=os.environ["APIFY_API_TOKEN"])

# Scrape website content using Apify
loader = apify.call_actor(
    actor_id="apify/website-content-crawler",
    run_input={
        "startUrls": [{"url": "https://www.example.com"}], # Replace with target URL
        "maxCrawlPages": 10
    },
    dataset_mapping_function=lambda item: Document(
        page_content=item["text"].replace('\n', ' ') or "",
        metadata={"source": item["url"], "title": item['metadata']["title"]}
    ),
)

# Load and chunk the scraped data
data = loader.load()
documents = chunk_data(data)

# Initialize and populate ChromaDB
db = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# Example search
query = "Enter your search query here"
results = semantic_search(query, db)

# Print results
for result in results:
    print(f"Content: {result.page_content[:200]}...")
    print(f"Source: {result.metadata['source']}")
    print(f"Title: {result.metadata['title']}\n")


# Alternative web scraping approaches with clean text extraction

def clean_text(text):
    """Clean extracted text by removing extra whitespace and normalizing"""
    import re
    # Normalize line breaks while preserving element separation
    text = re.sub(r'\s*\n\s*', '\n', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-\n]', '', text)
    return text.strip()


def scrape_with_beautifulsoup():
    """Scrape clean text content using BeautifulSoup"""
    import requests
    from bs4 import BeautifulSoup
    
    url = "https://www.example.com"  # Replace with target URL
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Remove unwanted elements
    for element in soup(['script', 'style', 'head', 'title', 'meta', '[document]']):
        element.decompose()
    
    # Extract text while preserving structure
    text_blocks = []
    for element in soup.find_all(['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        if element.get_text(strip=True):  # Only include non-empty elements
            text_blocks.append(element.get_text(strip=True))
    
    # Join blocks with newlines
    text = '\n'.join(text_blocks)
    clean_content = clean_text(text)
    
    # Get title separately
    title = clean_text(soup.title.string) if soup.title else ""
    
    return Document(
        page_content=clean_content,
        metadata={"source": url, "title": title, "timestamp": datetime.now().isoformat()}
    )

def scrape_with_playwright():
    """Scrape clean text content using Playwright"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto("https://www.example.com")  # Replace with target URL
            page.wait_for_load_state("networkidle")
            
            # Extract text content using JavaScript
            text = page.evaluate("""
                Array.from(document.querySelectorAll('body *'))
                    .filter(element => {
                        const style = window.getComputedStyle(element);
                        return style.display !== 'none' && 
                               style.visibility !== 'hidden' && 
                               !element.matches('script, style, meta');
                    })
                    .map(element => element.textContent)
                    .join(' ')
            """)
            
            clean_content = clean_text(text)
            title = clean_text(page.title())
            
            return Document(
                page_content=clean_content,
                metadata={"source": page.url, "title": title, "timestamp": datetime.now().isoformat()}
            )
            
        finally:
            browser.close()

# Example usage of text-focused scrapers
bs4_doc = scrape_with_beautifulsoup()
playwright_doc = scrape_with_playwright()

# Process and store clean text documents
clean_docs = [bs4_doc, playwright_doc]
chunked_docs = chunk_data(clean_docs)

# Add to existing ChromaDB
db.add_documents(documents=chunked_docs)

