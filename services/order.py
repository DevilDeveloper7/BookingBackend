import math
from datetime import datetime, date, timedelta
from operator import truediv, mod

from fastapi import HTTPException
from sqlalchemy import select

from const import base_table_available_places, date_format
from models.TableDto import TableBookDto, MultiPlyTableBookDto
from schemas.models import session, Table, Order, User


def create_order(table_dto: TableBookDto):
    available_table = session.get_one(Table, table_dto.id)

    order = Order(
        user_id=table_dto.user_id,
        table_id=available_table.id,
        total_price=calculate_table_price(table_dto, available_table),
        person_count=table_dto.person_count,
        start_booking_date_time=datetime.strptime(table_dto.booked_date_time, date_format),
        end_booking_date_time=datetime.strptime(table_dto.booked_date_time, date_format) + timedelta(hours=2)
    )
    session.add(order)
    session.commit()

    return order


def create_orders(table_dto: MultiPlyTableBookDto):
    temp = datetime.strptime(table_dto.booked_date_time, '%d.%m.%Y %H:%M')
    needed_tables_count = math.ceil(truediv(table_dto.person_count, base_table_available_places))
    filter_subq = session.query(Order.table_id).where(Order.start_booking_date_time <= temp).filter(
        Order.end_booking_date_time >= temp)
    available_tables = (session.scalars(
        select(Table)
        .where(Table.view == table_dto.view)
        .filter(Table.id.notin_(filter_subq)))
                        .all())

    if needed_tables_count > len(available_tables):
        raise HTTPException(status_code=404,
                            detail="Free tables with enough space for this date is not available")

    orders = []
    for table_i in range(needed_tables_count):
        order = Order(
            user_id=table_dto.user_id,
            table_id=available_tables[table_i].id,
            total_price=calculate_table_price(table_dto, available_tables[table_i]),
            start_booking_date_time=datetime.strptime(table_dto.booked_date_time, date_format),
            end_booking_date_time=datetime.strptime(table_dto.booked_date_time, date_format) + timedelta(hours=2)

        )
        if table_i != len(available_tables) - 1:
            order.person_count = mod(table_dto.person_count, available_tables[table_i].available_places)
        else:
            order.person_count = available_tables[table_i].available_places
        orders.append(order)
    session.add_all(orders)
    session.flush()
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


def find_orders_by_user_id_and_topic_id(user_id: int, topic_id: int):
    orders = session.query(select(Order).where(Order.user_id == user_id and Order.table_id == topic_id)).all()
    return orders


def find_orders_by_chat_id(chat_id: int):
    orders = session.scalars(select(Order)
                             .join(User)
                             .where(User.chat_id == chat_id)).all()
    return orders


def find_orders_by_user_id(user_id: int):
    orders = session.scalars(select(Order).where(Order.user_id == user_id
                                                 and Order.start_booking_date_time < datetime.now()
                                                 )).all()
    return orders
