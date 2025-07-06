from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from loader import db
from data.tranlations import conversations


class AdminKeyboardBuilder:
    def __init__(self):
        self.users = db.get_users()
        self.per_page = 5
        self.index = 0
        self.__call__()


    def __call__(self, *args, **kwds):
        self.users = db.get_users()
        buttons = []
        keyboards = []
        for user in self.users:
            buttons.append(
                InlineKeyboardButton(text=user[-1], callback_data=f"user_{user[0]}")
            )
        
        for i in range(0, len(self.users), self.per_page):
            keyboards.append(
                InlineKeyboardMarkup(inline_keyboard=[
                    [i] for i in buttons[i:i+self.per_page]
                ])
            )
        self.keyboards = keyboards
    
    def get_keyboard(self):
        try:
            current_kb = self.keyboards[self.index]
            self.index += 1
            return current_kb
        except IndexError:
            self.index = 0
            return None
        

class UserPromptBuilder:
    def __init__(self):
        self.per_page = 5
        self.index = 0
        self.keyboards = None
       



    def __call__(self, telegram_id, *args, **kwds):
        self.prompts = db.get_user_prompts(telegram_id)
        buttons = []
        keyboards = []
        if self.keyboards:
            return
        else:
            for prompt in self.prompts:
                buttons.append(
                    InlineKeyboardButton(text=prompt[-1], callback_data=f"prompt_{prompt[0]}")
                )
            
            for i in range(0, len(self.prompts), self.per_page):
                keyboards.append(
                    InlineKeyboardMarkup(inline_keyboard=[
                        [i] for i in buttons[i:i+self.per_page]
                    ]+[
                        [
                            InlineKeyboardButton(text="➡️", callback_data=f'user_{telegram_id}')
                        ]
                    ])
                )

            self.keyboards = keyboards
    
    def get_keyboard(self):
        try:
            current_kb = self.keyboards[self.index]
            self.index += 1
            return current_kb
        except IndexError:
            self.index = 0
            return None



def get_admin_kb(lang: str = 'uz'):
    data = conversations['admin'][lang]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=data[0])]
        ]
    )
