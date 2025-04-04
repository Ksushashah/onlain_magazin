
import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped,relationship
from models.cart import Cart



from settings.database import Base, connection, uniq_str_an


class User(Base):
    username: Mapped[uniq_str_an]
    email: Mapped[uniq_str_an]
    password: Mapped[str]
    
    
    cart: Mapped['Cart'] = relationship(
        'Cart',
        back_populates='user',
        uselist=False, 
        lazy='joined' 
    )
    
    orders : Mapped['Order'] = relationship(
        'Order',
        back_populates='user',
        cascade='all, delete-orphan',  
    )
    
    
    @classmethod
    @connection
    async def add(cls, 
            username: str, 
            email: str, 
            password: str,
            
            session: AsyncSession = None) -> dict[str, int]:
        
        existed_row =  await session.execute(select(cls).where(cls.username == username))
        user = existed_row.scalars().first() 
        if user:
            print(f'Пользователь {user.username} уже существует')
            return user

        
        hash_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(username=username, email=email, password=str(hash_pw)[2:-1])
    
        session.add(new_user)
        await session.flush() 
    
        cart = Cart(
            user_id = new_user.id,
            
        )
    
        session.add(cart)
        await session.commit()
        print(f'Создан пользователь с ID {new_user.id} и ему присвоена корзина -  {cart.id}')

        return {'user_id': new_user.id, 'cart_id': cart.id}

   
    def __str__(self):
        return f'[{self.id}] {self.username} | {self.email}'
