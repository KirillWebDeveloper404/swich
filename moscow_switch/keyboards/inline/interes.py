from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def interes_kb(data):
        kb = InlineKeyboardMarkup(row_width=2).add(
                        InlineKeyboardButton(text=f'{data["sport"]} Спорт', callback_data='sport'),
                        InlineKeyboardButton(text=f'{data["walk"]} Путешествия', callback_data='walk')
                ).add(
                        InlineKeyboardButton(text=f'{data["osozn"]} Осознанность', callback_data='osozn'),
                        InlineKeyboardButton(text=f'{data["mistik"]} Мистика', callback_data='mistik')
                ).add(
                        InlineKeyboardButton(text=f'{data["money"]} Финансы', callback_data='money'),
                        InlineKeyboardButton(text=f'{data["dance"]} Тусовки', callback_data='dance')
                ).add(
                        InlineKeyboardButton(text=f'{data["health"]} ЗОЖ', callback_data='health'),
                        InlineKeyboardButton(text=f'{data["alko"]} Винишко', callback_data='alko')
                ).add(
                        InlineKeyboardButton(text=f'{data["musik"]} Музыка', callback_data='musik'),
                        InlineKeyboardButton(text=f'{data["moda"]} Мода', callback_data='moda')
                ).add(
                        InlineKeyboardButton(text=f'Готово', callback_data='compleet')
                )
        return kb


def profi_kb(data):
        kb = InlineKeyboardMarkup(row_width=2).add(
                        InlineKeyboardButton(text=f'{data["market"]} Маркетинг', callback_data='market'),
                        InlineKeyboardButton(text=f'{data["konsalt"]} Консалтинг', callback_data='konsalt')
                ).add(
                        InlineKeyboardButton(text=f'{data["bloger"]} Блогер', callback_data='bloger'),
                        InlineKeyboardButton(text=f'{data["freelancer"]} Фрилансер', callback_data='freelancer')
                ).add(
                        InlineKeyboardButton(text=f'{data["design"]} Дизайнер', callback_data='design'),
                        InlineKeyboardButton(text=f'{data["shop"]} Торговля', callback_data='shop')
                ).add(
                        InlineKeyboardButton(text=f'{data["buissnes"]} Предприниматель', callback_data='buissnes'),
                        InlineKeyboardButton(text=f'{data["iskustvo"]} Творческий поиск', callback_data='iskustvo')
                ).add(
                        InlineKeyboardButton(text=f'{data["buti"]} Бьюти', callback_data='buti'),
                        InlineKeyboardButton(text=f'{data["it"]} Программист', callback_data='it')
                ).add(
                        InlineKeyboardButton(text=f'{data["psih"]} Психолог', callback_data='psih'),
                        InlineKeyboardButton(text=f'{data["eat"]} Рестораны', callback_data='eat')
                ).add(
                        InlineKeyboardButton(text=f'{data["stroy"]} Строительство', callback_data='stroy'),
                        InlineKeyboardButton(text=f'{data["soc"]} Соц работник', callback_data='soc')
                ).add(
                        InlineKeyboardButton(text=f'Готово', callback_data='compleet')
                )
        return kb