

from sqlalchemy import ForeignKey, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from models.enums import RatingEnum

from settings.database import Base, connection


class Review(Base):
    comment: Mapped[str]
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    rating: Mapped[RatingEnum] = mapped_column(default=RatingEnum.ONE, server_default=text("'ONE'"))

    product: Mapped['Product'] = relationship(
        'Product',
        back_populates='reviews',
    )
    @classmethod
    @connection
    def all_review(cls, product_id: int, session: Session = None):
        all_reviews = session.execute(select(cls).where(cls.product_id == product_id)).scalars().all()
        if not all_reviews:
            return 0 
        all_ratings = [int(rev.rating) for rev in all_reviews]
        avg_rating = sum(all_ratings) / len(all_ratings)
        session.commit() # надо комментить? 
        print(f"Средний рейтинг продукта {all_reviews[0].product.name}: {avg_rating}") # как в строчке 17? 
        return avg_rating

  
            
            

