from fastapi import APIRouter

router = APIRouter(
    prefix="/receipt",
    tags=["receipt"]
)


@router.get("/{user_id}")
async def get_receipt_by_user_id(user_id: int):
    pass
