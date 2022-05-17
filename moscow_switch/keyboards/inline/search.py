from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


search_kb = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text='🔍 Запустить поиск', callback_data='search')).add(
        InlineKeyboardButton(text='🧰 Профессия', callback_data='profi'),
        InlineKeyboardButton(text='🛠 Интересы', callback_data='interes')).add(
        InlineKeyboardButton(text='🔢 Возраст', callback_data='edit_age'),
        InlineKeyboardButton(text='📏 Рост', callback_data='edit_len')).add(
        InlineKeyboardButton(text='⚖️ Вес', callback_data='edit_weight')).add(
        InlineKeyboardButton(text='🔙 Главное меню', callback_data='main_menu'))


result_kb = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text='👍 Интересно', callback_data='like')).add(
        InlineKeyboardButton(text='➡️ Показать ещё', callback_data='next')).add(
        InlineKeyboardButton(text='⚙️ Изменить или остановить поиск', callback_data='edit_search'))