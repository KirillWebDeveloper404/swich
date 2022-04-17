from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_kb = ReplyKeyboardMarkup(
    [
        [KeyboardButton('👤Профиль')],
        [KeyboardButton('Актуальное на этой неделе')],
        [KeyboardButton('🔎Найти мероприятие'), KeyboardButton('🎭 Мои мероприятия')],
        [KeyboardButton('🫂Нетворкинг')],
        [KeyboardButton('📈Заказать рекламу'), KeyboardButton('💰Тарифы')],
        [KeyboardButton('❓О боте')],
    ],
    resize_keyboard=True
)
