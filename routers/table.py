from fastapi import APIRouter

from models.TableDto import TableBookDto
from services.table import book_table, book_tables

router = APIRouter(
    prefix="/tables",
    tags=["tables"]
)


@router.get("/all")
async def get_all_tables():
    pass


@router.post("/book")
async def book_table(table: TableBookDto):
    return book_table(table)


@router.post("/books")
async def book_tables(table: TableBookDto):
    return book_tables(table)


@router.get("/test")
def test():
    pass


@router.get("/{table_id}")
async def find_table(table_id: int):
    pass
