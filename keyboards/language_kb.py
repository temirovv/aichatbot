from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_language_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🇺🇿 UZ', callback_data='uz'),
             InlineKeyboardButton(text='🇺🇸 US', callback_data='en'),
             InlineKeyboardButton(text='🇷🇺 RU', callback_data='ru')]
        ]
    )
