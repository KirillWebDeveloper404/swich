from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


tarif_kb = ReplyKeyboardMarkup(
    [
        [KeyboardButton('1 месяц - 100р'), ],
        [KeyboardButton('3 месяца - 500р'), ],
        [KeyboardButton('6 месяцев - 1000р'), ],
        [KeyboardButton('Годовая подписка - 1500р'), ],
        [KeyboardButton('🔙 Главное меню'), ]
    ],
    resize_keyboard=True
)