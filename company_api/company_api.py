from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_name():
    """get name of company"""
    return {"company name":"sth like Snap, Ober"}