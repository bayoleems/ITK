from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.itk_service import ITKService

itk_service = ITKService()
scheduler = AsyncIOScheduler()

async def start_scheduler():
    scheduler.add_job(
        itk_service.scrape_and_store_data, 
        'cron', 
        args=['sample_data/companies.csv'], 
        hour=0, minute=0, second=0)
    scheduler.start()

async def stop_scheduler():
    scheduler.shutdown()