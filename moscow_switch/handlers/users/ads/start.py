from loader import dp, bot

from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from states import ADS
from sql import User, ADS_db


@dp.message_handler(Text(contains='заказать рекламу', ignore_case=True))
async def start(message: Message):
    await message.answer('Пришлите ссылку на основной сайт/паблик мероприятия\nОбязательно пришлите свой контакт для '
                         'связи\n\nВнимание заявки без указания контакта рассматриваться не будут',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[
                             [KeyboardButton('🔙Главное меню')]
                         ], resize_keyboard=True))
    await ADS.link.set()


@dp.message_handler(state=ADS.link)
async def link(message: Message, state: FSMContext):
    user = User.get(User.tg_id == message.from_user.id)
    ads = ADS_db()

    ads.name = user.name
    ads.phone = user.phone
    ads.link = message.text
    ads.save()

    await message.answer("Пришлите физический адрес где будет проходить мероприятие")
    await ADS.address.set()


@dp.message_handler(state=ADS.address)
async def address(message: Message, state: FSMContext):
    user = User.get(User.tg_id == message.from_user.id)
    ads = ADS_db.get(ADS_db.phone == user.phone)

    ads.addres = message.text
    ads.save()

    await message.answer("Напишите комментарий для модератора")
    await ADS.desc.set()


@dp.message_handler(state=ADS.desc)
async def desc(message: Message, state: FSMContext):
    user = User.get(User.tg_id == message.from_user.id)
    ads = ADS_db.get(ADS_db.name == user.name)

    ads.desc = message.text
    ads.save()

    await state.finish()
    await message.answer("Готово! \nОжидайте с вами скоро свяжутся...")
