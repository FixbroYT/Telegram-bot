import asyncio
from random import randint

from app.database.models import async_session
from app.database.models import User, Category, Item, UserItem
from sqlalchemy import select


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            new_user = User(tg_id=tg_id)
            session.add(new_user)
            await session.flush()
            await session.commit()

async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))

async def get_category_item(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category == category_id))

async def get_item(item_id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))

async def get_balance(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            return user.balance
        else:
            return 0

async def add_balance_once(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            return None

        item = await session.scalar(
            select(UserItem).where(UserItem.user_id == user.id, UserItem.item_id == 1)
        )

        if item:
            user.balance += 2
        else:
            user.balance += 1
        await session.commit()

async def buy_item(tg_id, item_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return None

        item_data = await session.scalar(select(Item).where(Item.id == item_id))

        if not item_data:
            return None

        if user.balance < item_data.price:
            return None

        data = await session.scalar(
            select(UserItem).where(UserItem.user_id == user.id, UserItem.item_id == item_id)
        )

        if data:
            return None

        user.balance -= item_data.price
        session.add(UserItem(user_id=user.id, item_id=item_id))

        await session.commit()
        return user.balance


async def get_items(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return []

        result = await session.scalars(
            select(Item).join(UserItem).where(UserItem.user_id == user.id)
        )
        if not result:
            return []

        return result.all()


async def passive_income_loop():
    while True:
        async with async_session() as session:
            users_with_passive_income = await session.scalars(select(User).join(UserItem).where(UserItem.item_id == 2))

            user_list = users_with_passive_income.all()
            user_list = set(user_list)

            for user in user_list:
                user.balance += 1

            await session.commit()
        await asyncio.sleep(1)

async def casino(tg_id, bet):
    try:
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))

            if not user:
                return None

            bet = float(bet)

            if bet > user.balance or bet > 100:
                return None

            user.balance -= bet

            random_num = randint(1, 100)

            coefficient = await session.scalar(select(UserItem).where(UserItem.user_id == user.id, UserItem.item_id == 3)
                                               )
            if coefficient:
                bet *= 1.5

            x = "0"

            if random_num <= 10:
                bet *= 4
                x = "4"
            elif 10 < random_num <= 25:
                bet *= 3
                x = "3"
            elif 30 < random_num <= 50:
                bet *= 2
                x = "2"
            elif random_num > 50:
                await session.commit()
                return "0", "0", "0"

            user.balance += bet

            await session.commit()

            return user.balance, bet, x, coefficient
    except ValueError:
        return None


async def profile(tg_id, user_name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            return None

        items_data = await session.scalars(select(UserItem).where(UserItem.user_id == user.id))
        items_data = items_data.all()

        if not items_data:
            items = "\n- No items"
        else:
            items = ""

        for item in items_data:
            item_name = await session.scalar(select(Item).where(Item.id == item.item_id))
            item_name = item_name.name
            items += "\n- " + item_name

        return f"📰 Profile {user_name}:\n\n💵 Balance:\n- {user.balance}$\n\n📦 Items: {items}"

async def sell_item(tg_id, item_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            return None

        item_data = await session.scalar(select(UserItem).where(UserItem.user_id == user.id, UserItem.item_id == item_id))

        if not item_data:
            return None

        item_info = await session.scalar(select(Item).where(Item.id == item_id))

        await session.delete(item_data)
        user.balance += item_info.price * 0.5
        await session.commit()
        return "Your item has been successfully sold for half price."