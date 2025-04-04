
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, relationship

from settings.database import Base, connection


class Category(Base):
    name: Mapped[str]
    
   
    product: Mapped['Product'] = relationship( 
        'Product',
        back_populates='category'
        
    )
    
    @classmethod
    @connection
    async def create_category(cls, name: str, session: AsyncSession = None):
        existed_row = await session.execute(select(cls).where(cls.name == name))
        category = existed_row.scalars().first() 
        if category:
            print(f"Категория {name} уже существует")
            return None
        new_category= Category(name=name)
        session.add(new_category)
        print(f'Категория {name} создана')
        await session.commit()
        return  new_category
    
    


