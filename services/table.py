import math
from datetime import datetime
from operator import truediv

from fastapi import HTTPException
from sqlalchemy import exists, select

from const import date_format, base_table_available_places
from models.TableDto import map_to_response
from schemas.models import session, Table, Order


def find_all():
    tables = session.query(Table).all()

    return tables


def find_table_short_info_by_id(table_id):
    return map_to_response(session.get_one(Table, table_id))


def check_table_available_on_date_time(table_id, date_time):
    tmp = datetime.strptime(date_time, date_format)
    table = session.scalar(
        exists()
        .where(Order.table_id == table_id)
        .where(Order.start_booking_date_time <= tmp)
        .where(Order.end_booking_date_time >= tmp)
        .select()
    )

    if table:
        return False
    else:
        return True


def check_is_enough_available_guest_places(guest_count: int, view: int, booked_date_time: str):
    temp = datetime.strptime(booked_date_time, '%d.%m.%Y %H:%M')
    needed_tables_count = math.ceil(truediv(guest_count, base_table_available_places))
    filter_subq = session.query(Order.table_id).where(Order.start_booking_date_time >= temp).filter(
        Order.end_booking_date_time <= temp)
    available_tables = (session.scalars(
        select(Table)
        .where(Table.view == view)
        .filter(Table.id.notin_(filter_subq)))
                        .all())

    if needed_tables_count > len(available_tables):
        raise HTTPException(status_code=404,
                            detail="Free tables with enough space for this date is not available")
    else:
        return True
