import asyncio
import argparse
from app.services.scheduler_service import start_scheduler, stop_scheduler
from app.services.itk_service import ITKService
from app.api.routers.itk import itk_banner
from app.utils.helpers import get_companies_from_csv
from app.utils.logging import logger

async def initial_scrape():
    """Perform initial scraping of company data"""
    try:
        itk = ITKService()
        await itk.scrape_and_store_data("sample_data/companies.csv")
    
    except Exception as e:
        logger.error(f"Error during initial scraping: {str(e)}")

async def chat_loop(company=None):
    """Interactive chat loop with ITK"""
    itk = ITKService()
    print(itk_banner())
    print("Welcome to ITK Chat!\n")
    
    while True:
        query = input("Enter your query (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        
        try:
            response = await itk.chat(query=query, company_name=company)
            print(f"ITK: {response}\n")
        except Exception as e:
            logger.error(f"Error during chat: {str(e)}")
            print("Sorry, there was an error processing your query. Please try again.")

async def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='ITK Chat Interface')
    parser.add_argument('--company', '-c', 
                       type=str,
                       help='Company name to focus the chat on',
                       choices=get_companies_from_csv("sample_data/companies.csv"),
                       default=None)
    args = parser.parse_args()

    # Start scheduler
    await start_scheduler()

    try:
        # Perform initial scrape
        await initial_scrape()
        
        # Start interactive chat loop
        await chat_loop(company=args.company)

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
    finally:
        # Clean shutdown
        await stop_scheduler()
        print("\nScheduler stopped. Goodbye!")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")
