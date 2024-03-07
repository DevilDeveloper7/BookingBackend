from fastapi import APIRouter

from models.TableDto import TableBookDto, MultiPlyTableBookDto
import services.table as service

router = APIRouter(
    prefix="/tables",
    tags=["tables"]
)


@router.get("/all")
async def get_all_tables():
    return service.find_all()


@router.post("/book")
async def book_table(table: TableBookDto):
    return service.book_table(table)


@router.post("/book/multiply")
async def book_tables(table: MultiPlyTableBookDto):
    return service.book_tables(table)


@router.get("/{table_id}")
async def find_table(table_id: int):
    pass
