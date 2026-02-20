from typing import Optional
from bot.db.models import UsersORM, ProductsORM, OrdersORM
from bot.db.database import async_engine, session_factory, Base

from sqlalchemy import select, and_
import logging

from bot.enums.enums import OrderStatuses

logger = logging.getLogger(__name__)

async def create_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        logger.info(f'tables created')
        
async def add_product(title : str, description : str, price : int, filepath : str) -> None:
    async with session_factory() as session:
        product = ProductsORM(
            title=title,
            description=description,
            price=price,
            filepath=filepath
        )
        
        session.add(product)
        await session.commit()
        
        logger.info(f'product {title} added')

async def select_product(id : int) -> Optional[ProductsORM]:
    async with session_factory() as session:
        product = await session.get(ProductsORM, id)
        return product
    
async def select_product_in_order(order_id : int) -> Optional[ProductsORM]:
    async with session_factory() as session:
        order = await session.get(OrdersORM, order_id)
        product = await session.get(ProductsORM, order.product_id)
        return product
    
async def select_all_products() -> Optional[list[ProductsORM]]:
    async with session_factory() as session:
        query = (select(ProductsORM))
        result = await session.execute(query)
        products = result.scalars().all()
        return products

async def select_all_products_from_orders(user_id : int) -> Optional[list[ProductsORM]]:
    async with session_factory() as session:
        query = (select(OrdersORM).where(and_(OrdersORM.user_id == user_id, OrdersORM.status == OrderStatuses.paid)))
        result = await session.execute(query)
        orders = result.scalars().all()
        products : Optional[list[ProductsORM]] = None
        for order in orders:
            product = session.get(ProductsORM, order.product_id)
            products.append(product)
        return products
            
            

async def add_user(id : int, username : str) -> None:
    async with session_factory() as session:
        query = (select(UsersORM).where(UsersORM.telegram_id == id))
        result = await session.execute(query)
        user = result.scalars().first()
        if user is None:
            logger.info(f'Пользователь {id} уже есть в БД')
            return
        
        user = UsersORM(
            telegram_id=id,
            username=username
        )
        session.add(user)
        logger.info(f'user {id} added')
        await session.commit()
        
async def insert_order(user_id : int, product_id : int, payment_id : str, status : OrderStatuses) -> Optional[int]:
    async with session_factory() as session:
        order = OrdersORM(
            user_id=user_id,
            product_id=product_id,
            payment_id=payment_id,
            status=status
        ) 
        session.add(order)
        await session.flush()
        order_id = order.id
        logger.info(f'order {order.id} added')
        await session.commit()
        return order_id
        
async def change_status_order(order_id : int, status : OrderStatuses, payment_id : str) -> Optional[OrdersORM]:
    async with session_factory() as session:
        order = await session.get(OrdersORM, order_id)
        order.status = status
        order.payment_id = payment_id
        await session.commit()