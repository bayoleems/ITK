from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from app.core.dependencies import get_itk_service
from app.services.itk_service import ITKService
from app.utils.logging import logger

router = APIRouter(prefix="/scrape", tags=["Scrape"])

@router.post("/scrape")
async def scrape(
    background_tasks: BackgroundTasks,
    itk_service: ITKService = Depends(get_itk_service),
):
    try:    
        background_tasks.add_task(
            itk_service.scrape_and_store_data, 
            "sample_data/companies.csv"
        )
        return {"message": "Scraping triggered successfully"}
    
    except Exception as e:
        logger.error(f"Error scraping and storing data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
