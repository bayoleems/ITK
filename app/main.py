from app.services.scheduler_service import start_scheduler, stop_scheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from app.api.routers import itk, scrape
from app.utils.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting ITK")
    await start_scheduler()
    yield
    # Shutdown
    logger.info("Shutting down ITK")
    await stop_scheduler()

app = FastAPI(
    title="ITK Platform",
    description="API for intelligent search",
    version="1.0.0",
    docs_url="/api-docs",
    docs_url_name="API Docs",
    lifespan=lifespan
)

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization", 
        "Accept",
        "Origin",
        "X-Requested-With"
    ],
    expose_headers=["Authorization"],
    max_age=600,
)

# Include routers
app.include_router(itk.router)
app.include_router(scrape.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 

@app.get("/")
async def root():
    return {
        "message": 
        "ITK!"
        }

if __name__ == "__main__":
    logger.info(itk.itk_banner())
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)