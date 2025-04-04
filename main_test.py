import asyncio

from models.category import Category
from models.user import User


async def create_user(username, email, password):
    user_data = await User.add(username=username, email=email, password=password)


async def create_category(name):
    create_category = await Category.create_category(name=name)


async def main():
    task1 = asyncio.create_task(create_category("Food"))

    await task1


if __name__ == "__main__":
    asyncio.run(main())
