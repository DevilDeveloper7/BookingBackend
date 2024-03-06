from pydantic import BaseModel

from schemas.models import User


class UserCreateDto(BaseModel):
    email: str
    first_name: str
    last_name: str
    contact_info: str
    chat_id: int


def convert_user_dto_to_entity(dto: UserCreateDto):
    return User(
        email=dto.email,
        first_name=dto.first_name,
        last_name=dto.last_name,
        contact_info=dto.contact_info,
        chat_id=dto.chat_id)


def update_user_entity_from_dto(entity: User, dto: UserCreateDto):
    entity.first_name = dto.first_name
    entity.last_name = dto.last_name
    entity.contact_info = dto.contact_info
    entity.chat_id = dto.chat_id
    return entity
