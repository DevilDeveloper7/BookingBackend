from datetime import datetime
from typing import List

from sqlalchemy import String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column, Session

from const import base_table_available_places
from database import Base, engine


class Restaurant(Base):
    __tablename__ = 'restaurant'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    tables: Mapped[List["Table"]] = relationship(back_populates="restaurant", cascade="all, delete-orphan")


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    contact_info: Mapped[str] = mapped_column(String, nullable=False)
    chat_id: Mapped[int] = mapped_column(Integer)
    orders: Mapped[List["Order"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Table(Base):
    __tablename__ = 'table'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    available_places: Mapped[int] = mapped_column(nullable=False, default=base_table_available_places)
    # In views 0 means Burj Khalifa view, 1 means Sea view
    view: Mapped[int] = mapped_column(nullable=False, default=0)
    # base for Burj Khalifa
    price: Mapped[int] = mapped_column(nullable=False, default=50)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurant.id"))
    restaurant: Mapped["Restaurant"] = relationship(back_populates="tables")
    order_info: Mapped[List["Order"]] = relationship(back_populates="table", cascade="all, delete-orphan")


class Order(Base):
    __tablename__ = 'order'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="orders")
    table_id: Mapped[int] = mapped_column(ForeignKey("table.id"))
    table: Mapped["Table"] = relationship(back_populates="order_info")
    person_count: Mapped[int] = mapped_column(default=0, nullable=False)
    total_price: Mapped[int] = mapped_column(default=0, nullable=False)
    booking_date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with Session(engine) as session:
    main_restaurant = Restaurant(
        name="Main Restaurant",
        tables=[
            Table(view=0, price=50),
            Table(view=0, price=50),
            Table(view=0, price=50),
            Table(view=1, price=80),
            Table(view=1, price=80),
            Table(view=1, price=80)
        ]
    )

    session.add(main_restaurant)
    session.commit()
