from typing import List
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship


from settings.database import Base, connection


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int] = mapped_column(default=0)
    category_id: Mapped[int] = mapped_column(ForeignKey('categorys.id'))

    cart_items:Mapped['Cart_Item'] = relationship(
        'Cart_Item',
        back_populates='product',  
        lazy='joined'
    )
    order_items:Mapped['Order_Item'] = relationship(
        'Order_Item', 
        back_populates='product',
        
        )
    category: Mapped['Category'] = relationship(
        'Category',
        back_populates='product',
    )

    reviews: Mapped['Review'] = relationship(
        'Review',
        back_populates='product',
        cascade='all, delete-orphan'
    )
    
    @classmethod
    @connection
    def create_product(cls, name: str, description: str, price: int, category_id: int, session: Session = None):
        existed_row = session.execute(select(cls).where(cls.name == name))
        category = existed_row.scalars().first() 
        if category:
            print(f"Продукт {name} уже существует")
            return None
        new_product= Product(name=name, description=description, price=price, category_id=category_id)
        session.add(new_product)
        print(f'Продукт {name} создан')
        session.commit()
        return  new_product


