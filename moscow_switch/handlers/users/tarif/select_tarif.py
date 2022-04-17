import datetime

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from loader import bot, dp

from sql.User import User
from states.tarifs import Tarif
from keyboards.default.main_menu import main_kb
from data.config import YOUKASSA_TOKEN


@dp.message_handler(state=Tarif.select)
async def bot_start(message: types.Message):

    try:

        if message.text == '1 месяц - 100р':
            await bot.send_invoice(
                message.chat.id,
                title='Подписка на месяц - 100р',
                description=f'Начало: сегодня. Действует до: {datetime.datetime.today() + datetime.timedelta(days=30)}',
                provider_token=YOUKASSA_TOKEN,
                currency='rub',
                prices=[{'label': 'руб', 'amount': 10000}],
                start_parameter='time-machine-example',
                payload='1_mouth'
            )

        elif message.text == '3 месяца - 500р':
            await bot.send_invoice(
                message.chat.id,
                title='Подписка на 3 месяца - 500р',
                description=f'Начало: сегодня. Действует до: {datetime.datetime.today() + datetime.timedelta(days=90)}',
                provider_token=YOUKASSA_TOKEN,
                currency='rub',
                prices=[{'label': 'руб', 'amount': 50000}],
                start_parameter='time-machine-example',
                payload='3_mouth'
            )

        elif message.text == '6 месяцев - 1000р':
            await bot.send_invoice(
                message.chat.id,
                title='Подписка на 6 месяцев - 1000р',
                description=f'Начало: сегодня. Действует до: {datetime.datetime.today() + datetime.timedelta(days=180)}',
                provider_token=YOUKASSA_TOKEN,
                currency='rub',
                prices=[{'label': 'руб', 'amount': 100000}],
                start_parameter='time-machine-example',
                payload='6_mouth'
            )

        elif message.text == 'Годовая подписка - 1500р':
            await bot.send_invoice(
                message.chat.id,
                title='Годовая подписка - 1500р',
                description=f'Начало: сегодня. Действует до: {datetime.datetime.today() + datetime.timedelta(days=365)}',
                provider_token=YOUKASSA_TOKEN,
                currency='rub',
                prices=[{'label': 'руб', 'amount': 150000}],
                start_parameter='time-machine-example',
                payload='1_year'
            )

    except Exception as e:
        pass


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT, state=Tarif.select)
async def payment_handler(message: types.Message, state: FSMContext):

    await state.finish()

    user = User.get(User.tg_id == message.from_user.id)
    if message.successful_payment.invoice_payload == '1_mouth':
        user.tarif = 'Подписка на месяц'
        user.dead_line = datetime.datetime.today() + datetime.timedelta(days=30)

    elif message.successful_payment.invoice_payload == '3_mouth':
        user.tarif = 'Подписка на 3 месяца'
        user.dead_line = datetime.datetime.today() + datetime.timedelta(days=90)

    elif message.successful_payment.invoice_payload == '6_mouth':
        user.tarif = 'Подписка на 6 месяцев'
        user.dead_line = datetime.datetime.today() + datetime.timedelta(days=180)
    
    elif message.successful_payment.invoice_payload == 'year':
        user.tarif = 'Годовая подписка'
        user.dead_line = datetime.datetime.today() + datetime.timedelta(days=365)
    
    user.save()

    await message.answer("Поздравляем, подписка на SWITCH оформлена! \n" \
                        "Наш  сервис  находится в удобном мессенджере Телеграм,  чтобы присоединиться к сервису пройдите по ссылке\n\n" \
                        "Если у вас не установлен телеграм, необходимо его скачать:\n" \
                        "Для Apple: https://apps.apple.com/ru/app/telegram/id686449807\n" \
                        "Для Android:" \
                        "https://play.google.com/store/apps/details?id=org.telegram.messenger&hl=ru&gl=US\n" \
                        "После установки телеграма, вернитесь. в это письмо и пройдите по ссылке!\n\n" \
                        "При возникновении трудностей, можете написать свой вопрос в ответном письме",
                        reply_markup=main_kb
                        )