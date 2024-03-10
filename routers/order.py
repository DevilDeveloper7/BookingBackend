import json

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.TableDto import TableBookDto, MultiPlyTableBookDto
from services.order import create_order, create_orders, find_orders_by_user_id

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


@router.get("/{user_id}")
async def get_receipt_by_user_id(user_id: int):
    orders = []
    for order in find_orders_by_user_id(user_id):
        orders.append(jsonable_encoder(order))
    # json_data = json.dumps(orders)
    return orders


@router.post("/book")
async def book_table(table: TableBookDto):
    return create_order(table)


@router.post("/book/multiply")
async def book_tables(table: MultiPlyTableBookDto):
    return create_orders(table)


@router.get("/{user_id}/{topic_id}")
async def get_receipt_by_user_id_and_topic_id(user_id: int):
    orders = []
    for order in find_orders_by_user_id(user_id):
        orders.append(jsonable_encoder(order))
    json_data = json.dumps(orders)
    return JSONResponse(content=json_data)
