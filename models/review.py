from sqlalchemy import ForeignKey, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.enums import RatingEnum
from models.product import Product
from settings.database import Base, connection


class Review(Base):
    comment: Mapped[str]
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    rating: Mapped[RatingEnum] = mapped_column(
        default=RatingEnum.ONE, server_default=text("'ONE'")
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="reviews",
    )

    @classmethod
    @connection
    async def all_review(cls, product_id: int, session: AsyncSession = None):
        all_reviews = (
            await session.execute(select(cls).where(cls.product_id == product_id))
            .scalars()
            .all()
        )
        if not all_reviews:
            return 0
        all_ratings = [int(rev.rating) for rev in all_reviews]
        avg_rating = sum(all_ratings) / len(all_ratings)
        product = (
            await session.execute(select(Product).where(Product.id == product_id))
            .scalars()
            .first()
        )
        print(f"Ищем продукт с ID {product_id}")
        if product is None:
            print(f"Продукт с ID {product_id} не найден")
            return None

        product.average_rating = avg_rating
        await session.commit()
        print(f"Средний рейтинг продукта {all_reviews[0].product.name}: {avg_rating}")
        return avg_rating
