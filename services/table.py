import math
from datetime import datetime, date
from operator import truediv

from fastapi import HTTPException
from sqlalchemy import select

from const import base_table_available_places
from models.TableDto import TableBookDto
from schemas.Receipt import Receipt
from schemas.models import session, Table


def book_table(table_dto: TableBookDto):
    available_table = session.scalars(select(Table).where(Table.id == table_dto.id))

    receipt = Receipt(0, table_dto.id, [available_table.id], calculate_table_price(table_dto, available_table),
                      [table_dto.booked_date_time])
    # available_table.booked_dates_times.append(table_dto.booked_date_time)

    # else:
    #     raise HTTPException(status_code=404, detail='Table with id {} not found'.format(table_dto.id))

    return receipt


def book_tables(table_dto: TableBookDto):
    available_tables = []
    needed_tables_count = math.ceil(truediv(table_dto.person_count, base_table_available_places))
    available_tables_count = 0
    db_tables = session.scalars(select(Table).where(Table.view == table_dto.view)).limit(needed_tables_count)

    if available_tables_count < db_tables.count():
        raise HTTPException(status_code=404,
                            detail="Free tables with enough space for this date is not available")

    receipt = Receipt(0, table_dto.id, [table.id for table in available_tables], 0,
                      [table_dto.booked_date_time])

    for table_i in range(len(available_tables)):
        receipt.total_cost += calculate_table_price(table_dto, available_tables[table_i])

    return receipt


def calculate_table_price(table_dto, table):
    if is_weekend(table_dto.booked_date_time):
        return table.price + 20
    return table.price


def is_weekend(date_str):
    # Checks if a given date string is a weekend.
    # Returns True, if given date string is a weekend, False otherwise.
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    return date_obj.weekday() >= 5


def checkDateTime(date_str):
    today = date.today()
    date_obj = datetime.strptime(date_str, '%Y-%m-%d %h-%m').date()
    if today <= date_obj:
        return True
    else:
        raise HTTPException(400, detail='Invalid date or time')
