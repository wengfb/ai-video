from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core import get_settings, setup_logging, get_logger, AppException
from app.api.v1 import router as api_v1_router

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    setup_logging()
    logger.info("Application starting", version=settings.app_version)
    yield
    logger.info("Application shutting down")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """应用异常处理"""
    return JSONResponse(
        status_code=400,
        content={"code": exc.code, "message": exc.message},
    )


# 注册路由
app.include_router(api_v1_router, prefix=settings.api_v1_prefix)


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "version": settings.app_version}
