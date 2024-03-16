from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Path

import services.table as service
from models.TableDto import map_to_response

router = APIRouter(
    prefix="/tables",
    tags=["tables"]
)


@router.get("/all")
async def get_all_tables():
    response_list = []
    for table in service.find_all():
        response_list.append(map_to_response(table))
    return response_list


@router.get("/{guest_count}/{view}/{date_time}")
async def check_is_enough_available_guest_places(guest_count: int, view: int, date_time: str):
    return service.check_is_enough_available_guest_places(guest_count, view, date_time)


@router.get("/{table_id}/{date_time}")
async def check_table_available_on_date_time(table_id: int, date_time: str):
    return service.check_table_available_on_date_time(table_id, date_time)


@router.get("/{table_id}")
async def find_table_short_info_by_id(table_id: Annotated[int, Path(title="The ID of the item to get")]):
    return service.find_table_short_info_by_id(table_id)
