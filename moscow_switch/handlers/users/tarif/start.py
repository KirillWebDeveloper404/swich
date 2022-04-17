from aiogram import types

from loader import dp, bot

from keyboards.default.tarif_kb import tarif_kb
from sql.User import User
from states.tarifs import Tarif
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text(contains='Тарифы', ignore_case=True))
async def bot_start(message: types.Message):

    try:

        user = User.get(User.tg_id == message.from_user.id)

        await Tarif.select.set()

        if user.tarif:
            await message.answer(f"Ваш тариф: {user.tarif} \n" \
                                f"Действует до {user.dead_line} \n" \
                                f"Хотите изменить тариф?",
                                reply_markup=tarif_kb)
        else:
            await message.answer(f"У вас нет тарифа, для использования сервиса выберите один тариф из списка и оплатите. Вы также можете сравнить тарифы",
                                reply_markup=tarif_kb)
    except:
        pass