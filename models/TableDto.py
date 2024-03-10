from pydantic import BaseModel


class TableBookDto(BaseModel):
    id: int
    person_count: int
    view: int
    user_id: int
    booked_date_time: str


class MultiPlyTableBookDto(BaseModel):
    person_count: int
    user_id: int
    view: int
    booked_date_time: str


class TableResponse(BaseModel):
    id: int
    view: int


def map_to_response(table):
    return TableResponse(id=table.id, view=table.view)
