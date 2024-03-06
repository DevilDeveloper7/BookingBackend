from fastapi import HTTPException
from sqlalchemy import exists, select
from sqlalchemy.exc import NoResultFound

from models.UserDto import UserCreateDto, convert_user_dto_to_entity, update_user_entity_from_dto
from schemas.models import session, User


def find_user(id: int):
    try:
        user = session.get_one(User, id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User with id = {0} not found".format(id))

    return user


def find_user_by_email(email: str):
    user = session.scalar_one(
        select(User)
        .filter_by(email=email)
    )
    if user:
        return user
    else:
        raise HTTPException(status_code=409, detail='User with email = {0} not found"'.format(email))


def create_user(dto: UserCreateDto):
    user = session.scalar(
        exists()
        .where(User.email == dto.email)
        .select()
    )
    if not user:
        user = convert_user_dto_to_entity(dto)
        session.add(user)
        session.flush()
    else:
        raise HTTPException(status_code=409, detail='This email {0} already registered in the system'.format(dto.email))

    return user


def update_user(dto: UserCreateDto):
    user = session.scalar_one(
        select(User)
        .filter_by(email=dto.email)
    )
    if user:
        update_user_entity_from_dto(user, dto)
        session.commit()
    else:
        raise HTTPException(status_code=409, detail="This user {0} doesn't registered in the system".format(dto.email))
    return user


def delete_user(user_id: int):
    session.delete(User, user_id)
