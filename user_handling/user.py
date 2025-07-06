from aiogram import html, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from loader import dp, db, ADMINS
from states.user_states import UserState
from keyboards.language_kb import get_language_kb

from data.tranlations import conversations
from aihandling.api_con import make_converstaion


@dp.message(F.func(lambda F: F.text == '/start' and F.from_user.id not in ADMINS))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    print(f"F.text == '/start' and F.from_user.id not in ADMINS = \
          {message.text == '/start' and message.from_user.id not in ADMINS}")
    user = message.from_user
    print(user)
    db.add_user(telegram_id=user.id, 
                full_name=user.full_name, 
                username=user.username,
                joined_at=message.date)
    
    text = """🇺🇸 Please Choose the language\n🇷🇺 Пожалуйста, выберите язык\n🇺🇿 Iltimos, tilni tanlang\n """

    await message.answer(
        text=text,
        reply_markup=await get_language_kb()
    )
    await state.set_state(UserState.lang)


@dp.callback_query(UserState.lang)
async def set_user_language(call: CallbackQuery, state: FSMContext):
    data = call.data
    user = call.from_user.id
    print(f"{data=}\n{user=}")
    db.update_user_language(user, data)
    await call.answer('language updated successfully!')
    text = conversations['level1'][data]
    await call.message.answer(text)
    await call.message.delete()
    await state.set_state(UserState.chat)


@dp.message(UserState.chat)
async def ai_chat_handler(message: Message, state: FSMContext):
    if message.text == '/start':
        await command_start_handler(message, state)

    prompt = message.text
    user = message.from_user
    lang = db.get_user_language(user.id)
    
    content = make_converstaion(prompt)

    if content:
        await message.answer(content)
        db.save_user_history(
            user_id=user.id,
            prompt=prompt,
            content=content,
            saved_at=message.date
            )
    else:
        await message.answer(conversations['errors'][lang])
