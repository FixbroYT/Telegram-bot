from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from app.database.requests import get_categories, get_category_item, get_items

from aiogram.utils.keyboard import InlineKeyboardBuilder


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Shop")],
    [KeyboardButton(text="Balance")],
    [KeyboardButton(text="Items")],
    [KeyboardButton(text="Casino")],
    [KeyboardButton(text="My Profile")]
], resize_keyboard=True)

balance_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="+", callback_data="+")]
])

sell_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Sell Item", callback_data="sell")]
])


async def sell_item_inline(tg_id):
    keyboard = InlineKeyboardBuilder()
    items = await get_items(tg_id)

    if not items:
        return InlineKeyboardMarkup(inline_keyboard=[])
    for item in items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"item3_{item.id}"))
    return keyboard.adjust(2).as_markup()

async def buy_item_inline(item_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Buy", callback_data=f"item2_{item_id}"))
    return keyboard.as_markup()

async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    return keyboard.adjust(1).as_markup()

async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'item_{item.id}'))
    return keyboard.adjust(2).as_markup()