from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from settings.database import Base


class Cart_Item(Base):
    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(default=0)
    
    cart: Mapped['Cart'] = relationship(
        'Cart',
        back_populates='cart_items'
    )
    
    product:Mapped['Product'] = relationship(
        'Product',
        back_populates='cart_items', 
        lazy='joined'
    )