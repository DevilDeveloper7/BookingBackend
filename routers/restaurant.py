from fastapi import APIRouter

from schemas.models import main_restaurant

router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"]
)


@router.get("/")
async def get_all_restaurants():
    return main_restaurant
