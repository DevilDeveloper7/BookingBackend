from pydantic import BaseModel


class TableBookDto(BaseModel):
    id: int
    person_count: int
    user_id: int
    booked_date_time: str
