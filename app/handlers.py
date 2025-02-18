from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq
from app.database.requests import get_balance, add_balance_once

from app.keyboards import categories


router = Router()


class Casino(StatesGroup):
    bet = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer("👋 Hello!")
    await message.answer("⚙️ Choose an option:", reply_markup=kb.main)


@router.message(F.text == "Shop")
async def store(message: Message):
    await message.answer("📁 Select a category:", reply_markup=await categories())


@router.message(F.text == "Balance")
async def show_balance(message: Message):
    balance = await get_balance(message.from_user.id)
    await message.answer(f"💳 Your balance: {balance}$", reply_markup=kb.balance_inline)


@router.callback_query(F.data == "+")
async def add_balance(callback: CallbackQuery):
    await add_balance_once(callback.from_user.id)
    await callback.message.edit_text(f"💳 Your balance: {await get_balance(callback.from_user.id)}$",
                                     reply_markup=kb.balance_inline)


@router.callback_query(F.data.startswith("category_"))
async def category(callback: CallbackQuery):
    await callback.message.answer("📦 Select an item from this category:",
                                reply_markup=await kb.items(callback.data.split("_")[1]))


@router.callback_query(F.data.startswith("item_"))
async def item(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split("_")[1])
    await callback.message.answer(f"📄 {item_data.name} - {item_data.description}.\n💰 Price: {item_data.price}.",
                                reply_markup=await kb.buy_item_inline(item_data.id))


@router.callback_query(F.data.startswith("item2_"))
async def buy_item_handler(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split("_")[1])
    new_balance = await rq.buy_item(tg_id=callback.from_user.id, item_id=item_data.id)

    if new_balance is None:
        await callback.message.answer("❌ Error: Purchase failed! Check your balance or item availability.")
        return

    await callback.message.edit_text(f"✔️ You successfully purchased the item!\n💳 Your new balance: {new_balance}$")


@router.message(F.text == "Items")
async def show_items(message: Message):
    items = await rq.get_items(message.from_user.id)
    if items:
        text = "📦 Your items:\n" + "\n".join(f"- {item.name}" for item in items)
        await message.answer(text, reply_markup=kb.sell_inline)
    else:
        await message.answer("❌ You don't have any items yet!")


@router.callback_query(F.data == "sell")
async def sell_item(callback: CallbackQuery):
    await callback.message.edit_text("Select the item you want to sell:", reply_markup=await kb.sell_item_inline(callback.from_user.id))


@router.callback_query(F.data.startswith("item3_"))
async def sell_item_2(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split("_")[1])
    await callback.answer(await rq.sell_item(callback.from_user.id, item_data.id))


@router.message(F.text == "Casino")
async def casino_state(message: Message, state: FSMContext):
    await state.set_state(Casino.bet)
    await message.answer("💰 Enter your bet (max: 100): ")


@router.message(Casino.bet)
async def casino(message: Message, state: FSMContext):
    await state.update_data(bet=message.text)
    data = await state.get_data()
    casino_data = await rq.casino(message.from_user.id, data["bet"])
    if casino_data is None:
        await message.answer("❌ Error! Check your input.")
        await state.clear()
        return
    else:
        new_balance = casino_data[0]
        bet = casino_data[1]
        x = casino_data[2]
        if len(casino_data) == 4:
            coefficient = casino_data[3]
        else:
            coefficient = False

    if new_balance == "0":
        await message.answer("😓 Unfortunately, you lost...")
    else:
        if coefficient:
            await message.answer(f"🎉 Your bet won with a multiplier: {x}X + 1.5X!\n💸 You earned: {bet}$.\n💳 Your new balance: {new_balance}$.")
        else:
            await message.answer(f"🎉 Your bet won with a multiplier: {x}X!\n💸 You earned: {bet}$.\n💳 Your new balance: {new_balance}$.")
    await state.clear()


@router.message(F.text == "My Profile")
async def profile(message: Message):
    await message.answer(await rq.profile(message.from_user.id, message.from_user.full_name))
