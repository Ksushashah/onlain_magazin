import heapq

from sqlalchemy import ForeignKey, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from settings.database import Base, connection


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int] = mapped_column(default=0)
    category_id: Mapped[int] = mapped_column(ForeignKey("categorys.id"))
    average_rating: Mapped[float] = mapped_column(
        default=0.0, server_default=text("'0.0'")
    )

    cart_items: Mapped["Cart_Item"] = relationship(
        "Cart_Item",
        back_populates="product",
    )
    order_items: Mapped["Order_Item"] = relationship(
        "Order_Item",
        back_populates="product",
    )
    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="product",
    )

    reviews: Mapped["Review"] = relationship(
        "Review", back_populates="product", cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"{self.id}  | {self.name} | {self.price} рублей"

    @classmethod
    @connection
    async def create_product(
        cls,
        name: str,
        description: str,
        price: int,
        category_id: int,
        average_rating: float = 0,
        session: AsyncSession = None,
    ):
        existed_row = await session.execute(select(cls).where(cls.name == name))
        product = existed_row.scalars().first()
        if product:
            print(f"Продукт {name} уже существует")
            return None
        new_product = Product(
            name=name,
            description=description,
            price=price,
            category_id=category_id,
            average_rating=average_rating,
        )
        session.add(new_product)
        print(f"Продукт {name} создан")
        await session.commit()
        return new_product

    @classmethod
    @connection
    async def search_by_category_and_price(
        cls,
        category_id: str,
        min_price: int,
        max_price: int,
        session: AsyncSession = None,
    ):
        products = (
            await session.execute(
                select(cls).where(
                    cls.category_id == category_id,
                    cls.price >= min_price,
                    cls.price <= max_price,
                )
            )
            .scalars()
            .all()
        )
        print("Товары в вашем диапазоне:")
        return [print(x) for x in products]

    @classmethod
    @connection
    async def top(cls, session: AsyncSession = None):
        result = await session.execute(select(cls))
        products = result.scalars().all()

        rated_products = [
            (product.average_rating, product)
            for product in products
            if product.average_rating is not None
        ]
        if not rated_products:
            print("Нет товаров с рейтингом.")
            return []

        # Получаем топ-5 товаров по рейтингу
        top_products = heapq.nlargest(5, rated_products, key=lambda x: x[0])

        # Выводим товары
        for rating, product in top_products:
            print(f"Товар: {product.name}, Средний рейтинг: {rating}")

        return top_products
