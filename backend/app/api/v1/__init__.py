from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def api_root():
    """API 根路径"""
    return {"message": "AI Video API v1"}
