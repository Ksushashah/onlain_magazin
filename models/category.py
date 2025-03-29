
from sqlalchemy import select
from sqlalchemy.orm import Mapped, Session, relationship

from settings.database import Base, connection


class Category(Base):
    name: Mapped[str]
    
   
    product: Mapped['Product'] = relationship( 
        'Product',
        back_populates='category'
        
    )
    
    @classmethod
    @connection
    def create_category(cls, name: str, session: Session = None):
        existed_row = session.execute(select(cls).where(cls.name == name))
        category = existed_row.scalars().first() 
        if category:
            print(f"Категория {name} уже существует")
            return None
        new_category= Category(name=name)
        session.add(new_category)
        print(f'Категория {name} создана')
        session.commit()
        return  new_category
    
    


