import math
from datetime import datetime, date
from operator import truediv, mod

from fastapi import HTTPException
from sqlalchemy import select

from const import base_table_available_places
from models.TableDto import TableBookDto, map_to_response, MultiPlyTableBookDto
from schemas.models import Order
from schemas.models import session, Table

date_format = '%d.%m.%Y %H:%M'


def find_all():
    response_list = []
    tables = session.query(Table).all()
    for table in tables:
        response_list.append(map_to_response(table))
    return response_list


def book_table(table_dto: TableBookDto):
    available_table = session.get_one(Table, table_dto.id)

    order = Order(
        user_id=table_dto.user_id,
        table_id=available_table.id,
        total_price=calculate_table_price(table_dto, available_table),
        person_count=table_dto.person_count,
        booking_date_time=datetime.strptime(table_dto.booked_date_time, date_format)
    )
    session.add(order)
    session.commit()

    return order


def book_tables(table_dto: MultiPlyTableBookDto):
    needed_tables_count = math.ceil(truediv(table_dto.person_count, base_table_available_places))
    available_tables = (session.scalars(
        select(Table)
        .join(Order, Table.id == Order.table_id)
        .where(
            Table.view == table_dto.view)
        .filter(Order.booking_date_time != table_dto.booked_date_time)
        .limit(needed_tables_count)).all())

    if needed_tables_count < len(available_tables):
        raise HTTPException(status_code=404,
                            detail="Free tables with enough space for this date is not available")

    orders = []
    for table_i in range(len(available_tables)):
        order = Order(
            user_id=table_dto.user_id,
            table_id=available_tables[table_i].id,
            total_price=calculate_table_price(table_dto, available_tables[table_i]),
            booking_date_time=datetime.strptime(table_dto.booked_date_time, date_format)
        )
        if table_i != len(available_tables) - 1:
            order.person_count = mod(table_dto.person_count, available_tables[table_i].available_places)
        else:
            order.person_count = available_tables[table_i].available_places
        orders.append(order)
    session.add_all(orders)
    session.commit()
    return orders


def calculate_table_price(table_dto, table):
    if is_weekend(table_dto.booked_date_time):
        return table.price + 20
    return table.price


def is_weekend(date_str):
    # Checks if a given date string is a weekend.
    # Returns True, if given date string is a weekend, False otherwise.
    date_obj = datetime.strptime(date_str, date_format).date()
    return date_obj.weekday() >= 5


def checkDateTime(date_str):
    today = date.today()
    date_obj = datetime.strptime(date_str, date_format).date()
    if today <= date_obj:
        return True
    else:
        raise HTTPException(400, detail='Invalid date or time')
