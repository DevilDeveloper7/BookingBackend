from fastapi import FastAPI

from routers.restaurant import router as restaurant_router
from routers.table import router as table_router
from routers.user import router as user_router
from routers.order import router as order_router

app = FastAPI()

app.include_router(restaurant_router)
app.include_router(table_router)
app.include_router(user_router)
app.include_router(order_router)
