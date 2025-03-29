
from sqlalchemy import  ForeignKey, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from models.enums import StatusEnum


from settings.database import Base, connection


class Order(Base):
    total_price:Mapped[int] = mapped_column(default=0)
    status: Mapped[StatusEnum] = mapped_column(
        default=StatusEnum.IN_PROGRESS,
        server_default=text("'DRAFT'")
    )
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id')) 
    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id'))
    user: Mapped['User'] = relationship(
        'User',
        back_populates='orders', 
    )

    order_items: Mapped['Order_Item'] = relationship(
        'Order_Item',
        back_populates='order',
        cascade='all, delete-orphan',
        lazy = 'joined')
    
    cart: Mapped['Cart'] = relationship(
        'Cart',
        back_populates='orders', 
    )
    
    @classmethod
    @connection
    def update_status(cls, order_id: int, new_status: StatusEnum, session: Session = None):
        order = session.execute(select(cls).where(cls.id == order_id)).scalars().first()
        if not order:
            return f"Заказ с id {order_id} не найден"
        order.status = new_status
        session.commit() 
        return f"Статус заказа {order_id}  обновлен на {new_status}"
