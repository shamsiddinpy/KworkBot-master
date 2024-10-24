from aiogram import types, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import update, select
from aiogram.types import BotCommand
from bot.button.reply import language_button, main_menu
from bot.button.text import begin_text
from bot.language import data
from bot.state import UserState
from bot.utils import task_design
from db.config import session
from db.model import Task, Customer, Freelancer, User
from dispatcher import dp


@dp.message(CommandStart())
async def start_handler(msg: Message, state: FSMContext):
    query = select(Customer).where(Customer.user_id == msg.from_user.id)
    user_query = select(User).where(User.telegram_id == msg.from_user.id)
    user_result = session.execute(user_query).fetchone()
    if user_result is None:
        new_user = User(
            telegram_id=msg.from_user.id,
            username=msg.from_user.username,
        )
        session.add(new_user)
        session.commit()
    customer = session.execute(query).fetchone()
    if not customer:
        await msg.answer(begin_text)
        await state.set_state(UserState.language)
        await msg.answer("Tilni tanlang 👇 ", reply_markup=language_button())
    else:
        customer = customer[0]
        await state.set_data(customer.__dict__)
        await msg.answer("Asosiy menu", reply_markup=main_menu(customer.lang))


@dp.message(lambda msg: msg.text in ("🇺🇿 UZB", "🇬🇧 ENG"), UserState.language)
async def language_handler(msg: Message, state: FSMContext):
    lang = msg.text.split()[1]
    state_data = await state.get_data()
    state_data.update({"lang": lang})
    await state.set_data(state_data)
    text = data[lang]['welcome']
    await msg.answer(text, reply_markup=main_menu(lang))


@dp.message(lambda msg: msg.text == data['UZB']['language'])
@dp.message(lambda msg: msg.text == data['ENG']['language'])
async def language_handler(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    await state.set_state(UserState.language)
    await msg.answer(data[lang]['choose_lang'], reply_markup=language_button())


@dp.callback_query(lambda call: call.data.startswith("accept"))
@dp.callback_query(lambda call: call.data.startswith("ignore"))
async def confirm_answer(call: types.CallbackQuery, state: FSMContext):
    mode, task_id = call.data.split("_")
    select_query = select(Task).where(Task.id == task_id)
    task = session.execute(select_query).fetchone()[0]
    if mode == "accept":
        status = "ACCEPT"
        q = select(Freelancer.user_id).where(task.category_id == Freelancer.category_id)
        freelancers_id = session.execute(q).fetchall()
        task_text = task_design.format(task.id, task.category.name, task.title, task.description, task.price)
        for chat_id in freelancers_id:
            await call.message.bot.send_message(chat_id[0], text=task_text)
    else:
        status = "IGNORE"
    query = update(Task).values({"status": status}).where(Task.id == task_id)
    session.execute(query)

    session.commit()
    await call.message.delete()
    await call.message.bot.send_message(task.customer.user_id, text=f"Sizning buyurtmangiz statusi : 🟢{status}")


@dp.message(Command("count"))
async def count_handler(msg: types.Message, state: FSMContext):
    customer_count = await Customer.count()
    await msg.answer(f"Total customers: {customer_count}")
