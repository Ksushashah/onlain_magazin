from math import prod
from models.cart import Cart
from models.category import Category
from models.enums import RatingEnum, StatusEnum
from models.order import Order
from models.product import Product
from models.review import Review
from models.user import User
from settings.database import DATABASE_URL


if __name__=="__main__":
    '''User.add(username='Admin', email='admin@ya.ru', password='password')
    print(DATABASE_URL)'''
    
    '''Category.create_category(name='Electronics')
    Category.create_category(name='Food')
    Category.create_category(name='Clothes')
    Product.create_product(name='Laptop', description='New laptop', price=1000, category_id=15)
    Product.create_product(name='Apple', description='New apple', price=20, category_id=16)
    Product.create_product(name='Shirt', description='New shirt', price=50, category_id=17)
    Cart.add_cart(user_id=1, product_id=1, quantity=1)
    Cart.place_order(user_id=1)'''
    '''Order.update_status(order_id=2, new_status=StatusEnum.DONE)'''
    '''Review.add(comment='Good laptop', rating=RatingEnum.FIVE, product_id=1)
    Review.add(comment='BAD laptop', rating=RatingEnum.ONE, product_id=1)
    Review.all_review(product_id=1)'''
    '''Product.create_product(name='T-shirt', description='New shirt', price=50, category_id=17)'''
    '''Cart.add_cart(user_id=1, product_id=1, quantity=1)'''
    '''Cart.remove_product(user_id=1,product_id=1,quantity=2)'''
    '''User.add(username='Ksenia', email='ksenia@ya.ru', password='ksenia')
    Category.create_category(name='Candy')
    Product.create_product(name='Candy', description='New candy', price=30, category_id=16)
    Product.delete_per_id(id=6)'''
    '''Product.create_product(name='Candy', description='New candy', price=30, category_id=18)
    Cart.add_product(user_id=2, product_id=5, quantity=1)
    Cart.add_product(user_id=2, product_id=7, quantity=20)
    Cart.add_product(user_id=1, product_id=1, quantity=10)'''
    '''Cart.remove_product(user_id=2,product_id=7,quantity=2)'''
    '''Review.add(comment='Good candy', rating=RatingEnum.SEVEN, product_id=7)'''
    Review.all_review(product_id=1)
    Review.all_review(product_id=7)
    Cart.place_order(user_id=1)
    

