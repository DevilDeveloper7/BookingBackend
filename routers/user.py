from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import services.user as service
from models.UserDto import UserCreateDto

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/user/{id}")
async def find_user(id: int):
    return service.find_user(id)

@router.get("/user/chat/{chat_id}")
async def find_user(chat_id: int):
    return service.find_user_by_chat_id(chat_id)


@router.get("/user")
async def find_user_by_email(email: str):
    return service.find_user_by_email(email)


@router.post("/user")
async def create_user(dto: UserCreateDto):
    user = service.create_user(dto)
    json_data = jsonable_encoder(user)
    return JSONResponse(content=json_data)


@router.put("/user")
async def update_user(dto: UserCreateDto):
    return service.update_user(dto)


@router.delete("/user/{id}")
async def delete_user(id: int):
    return service.delete_user(id)
