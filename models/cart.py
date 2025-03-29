
from sqlalchemy import ForeignKey, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from models.cartItem import Cart_Item




from models.order import Order
from models.orderitem import Order_Item
from settings.database import Base, connection


class Cart(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True) 
    user: Mapped['User'] = relationship(
        'User',
        back_populates='cart',
        uselist=False,
    )
    cart_items: Mapped[list['Cart_Item']] = relationship(
        'Cart_Item',
        back_populates='cart',
        cascade='all, delete-orphan',
        lazy='joined',
        uselist=True)
        
    
    
    orders : Mapped['Order'] = relationship(
        'Order',
        back_populates='cart',
          
    )
    
    @classmethod
    @connection
    def add_product(cls, user_id: int, product_id: int, quantity: int, session: Session = None):
        existed_row = session.execute(select(cls).where(cls.user_id == user_id))
        cart = existed_row.scalars().first()
        if not cart:
            cart = cls(user_id=user_id)
            session.add(cart)
            session.commit() 
        cart_item = session.execute(select(Cart_Item).where(Cart_Item.cart_id == cart.id, Cart_Item.product_id == product_id)).scalars().first()
        if cart_item:
            cart_item.quantity += quantity
            print(f'Продукт {product_id} увеличен')
        else:
            cart_item = Cart_Item(cart_id=cart.id, product_id=product_id, quantity=quantity)
            session.add(cart_item)
            print(f'Продукт {product_id} добавлен')

        session.commit()  
        session.refresh(cart)
        return cart
       
    @classmethod
    @connection
    def remove_product(cls, user_id: int, product_id: int, quantity: int = None, session: Session = None):
            cart = session.execute(select(cls).where(cls.user_id == user_id)).scalars().first()
            if not cart:
                return None 
            cart_item = session.execute(select(Cart_Item).where(Cart_Item.cart_id == cart.id, Cart_Item.product_id == product_id)).scalars().first()
            if not cart_item:
                return None 
            if cart_item.quantity > quantity:
                cart_item.quantity -= quantity
                print(f'Продукт {product_id} уменьшен на {quantity} шт')
                session.commit() 
            else:
                
                session.delete(cart_item)
                print(f'Продукт {product_id} удален')
                session.commit() 
            
            
            session.refresh(cart) 
            return cart

        
    @classmethod
    @connection
    def place_order(cls, user_id: int, session: Session = None):
        cart = session.execute(select(cls).where(cls.user_id == user_id)).scalars().first()
        if not cart:
            return None 
        total_price = 0.0
        order_items = []  
        for cart_item in cart.cart_items: 
            total_price += cart_item.quantity * cart_item.product.price
            order_items.append({
                'product_id': cart_item.product_id,
                'quantity': cart_item.quantity,
                'price': cart_item.product.price,
            })

        order = Order(user_id=user_id, total_price=total_price,cart_id=cart.id)
        session.add(order)
        session.flush()  

        for item in order_items:
            order_item = Order_Item(
                order_id=order.id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                price_at_time=item['price']
            )
            session.add(order_item)

        Cart_Item.delete_per_id(cart.id)
        session.query(Cart_Item).filter(Cart_Item.cart_id == cart.id).delete()
        session.commit() 
        session.refresh(order) 
        print(f'Заказ {order.id} создан')

        return order
