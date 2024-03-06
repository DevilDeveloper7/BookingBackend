from fastapi import APIRouter

import services.user as service
from models.UserDto import UserCreateDto

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/user/{id}")
async def find_user(id: int):
    return service.find_user(id)


@router.get("/user")
async def find_user_by_email(email: str):
    return service.find_user_by_email(email)


@router.post("/user")
async def create_user(dto: UserCreateDto):
    return service.create_user(dto)


@router.put("/user")
async def update_user(dto: UserCreateDto):
    return service.update_user(dto)


@router.delete("/user/{id}")
async def update_user(id: int):
    return service.delete_user(id)
