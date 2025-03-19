from typing import Optional, Literal
from fastapi import APIRouter, Depends, HTTPException, Form
from app.core.dependencies import get_itk_service
from app.services.itk_service import ITKService
from app.utils.logging import logger
from app.utils.helpers import get_companies_from_csv

router = APIRouter(prefix="/itk", tags=["ITK"])
companies = get_companies_from_csv("sample_data/companies.csv")


@router.post("/chat")
async def chat_itk(
    query: str = Form(..., description="query"),
    company_name: Optional[Literal[*companies]] = Form(None, description="company"),
    itk_service: ITKService = Depends(get_itk_service),
):
    try:        
        response = await itk_service.chat(
            query=query,
            company_name=company_name
        )
        return response
        
    except Exception as e:
        logger.error(f"Error chatting with ITK")
        raise HTTPException(status_code=500, detail=str(e))

def itk_banner():
    return """
██╗████████╗██╗  ██╗
██║╚══██╔══╝██║ ██╔╝
██║   ██║   █████╔╝ 
██║   ██║   ██╔═██╗ 
██║   ██║   ██║  ██╗
╚═╝   ╚═╝   ╚═╝  ╚═╝
"""
