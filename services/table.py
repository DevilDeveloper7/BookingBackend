from models.TableDto import map_to_response
from schemas.models import session, Table


def find_all():
    tables = session.query(Table).all()

    return tables


def find_table_short_info_by_id(table_id):
    return map_to_response(session.get_one(Table, table_id))
