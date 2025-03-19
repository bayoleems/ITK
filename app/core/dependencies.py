from functools import lru_cache
from app.services.itk_service import ITKService

_itk_service = None

@lru_cache()
def get_itk_service() -> ITKService:
    """Get or create ITKService instance"""
    global _itk_service
    
    if _itk_service is None:
        _itk_service = ITKService()
        
    return _itk_service