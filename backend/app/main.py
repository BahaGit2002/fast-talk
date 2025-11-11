import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    description="Real-time chat application with WebSocket support",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# # Подключение роутеров
# app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
# app.include_router(chat.router, prefix=settings.API_V1_PREFIX)
# app.include_router(upload.router, prefix=settings.API_V1_PREFIX)
# app.include_router(groups.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
        "environment": settings.ENVIRONMENT
    }
