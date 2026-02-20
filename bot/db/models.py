from bot.db.database import Base
from bot.enums.enums import OrderStatuses

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, Text, text, ARRAY, BigInteger
from typing import Annotated
from datetime import datetime

intpk = Annotated[int, mapped_column(primary_key=True)]
create_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

class UsersORM(Base):
    __tablename__ = "users"
    id : Mapped[intpk]
    telegram_id : Mapped[int] = mapped_column(BigInteger, unique=True)
    username : Mapped[str] = mapped_column(nullable=True)
    created_at : Mapped[create_at]
    
class ProductsORM(Base):
    __tablename__ = "products"
    id : Mapped[intpk]
    title : Mapped[str]
    description : Mapped[str]
    price : Mapped[int]
    file_path : Mapped[str] = mapped_column(nullable=False)
    
class OrdersORM(Base):
    __tablename__ = "orders"
    id : Mapped[intpk]
    user_id : Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id"))
    product_id : Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id"))
    payment_id : Mapped[str] = mapped_column(nullable=True)
    status : Mapped[OrderStatuses]
    created_at : Mapped[create_at]