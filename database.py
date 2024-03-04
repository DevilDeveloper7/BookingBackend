from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_engine('sqlite:///booking_db.sqlite3', echo=True)


class Base(DeclarativeBase):
    pass
