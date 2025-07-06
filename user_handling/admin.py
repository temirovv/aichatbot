from aiogram import html
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F

from loader import dp, db, ADMINS
from keyboards.admin_kb import AdminKeyboardBuilder, get_admin_kb, UserPromptBuilder
from data.tranlations import conversations


commands = ["Foydalanuvchilar tarixini ko'rish","View user history", "Посмотреть историю пользователя"]
keyboard  = AdminKeyboardBuilder()
prompt_builder = UserPromptBuilder()

@dp.message(CommandStart(), F.from_user.id.in_(ADMINS))
async def admin_start_handler(message: Message, state: FSMContext):
    await message.answer("Salom hurmatli admin",  reply_markup=get_admin_kb())
    

@dp.message(F.text.in_(commands), F.from_user.id.in_(ADMINS))
async def show_user_history(message: Message, state: FSMContext):
    keyboard()
    kb = keyboard.get_keyboard()
    lang = message.from_user.language_code.lower()
    if kb:
        await message.answer(conversations['admin'][lang][1], reply_markup=kb)


@dp.callback_query(F.data.startswith('user'))
async def show_user_prompts(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split('_')[-1]
    prompt_builder(telegram_id=user_id)
    kb = prompt_builder.get_keyboard()
    lang = call.from_user.language_code.lower()
    await call.answer('👀')

    if kb:
        await call.message.edit_text(conversations['admin'][lang][2], reply_markup=kb)


@dp.callback_query(F.data.startswith('prompt'))
async def show_user_prompts_answer(call: CallbackQuery, state: FSMContext):
    history_id = call.data.split('_')[-1]
    history = db.get_content_by_prompt(history_id)[0]
    await call.answer('👀')
    await call.message.answer(history)

