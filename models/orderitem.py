from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship



from settings.database import Base


class Order_Item(Base):
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(default=1)
    price_at_time: Mapped[int]=mapped_column(default=0)
    
    order: Mapped['Order'] = relationship(
        'Order',
        back_populates='order_items'
    )
    
    product: Mapped['Product'] = relationship(
        'Product',
        back_populates='order_items',
        lazy='joined'
        )