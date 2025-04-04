from datetime import datetime
from aiogram import F, Router, html
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.formatting import Bold, HashTag, as_key_value, as_list, as_marked_section


r = Router()


@r.message(Command("start"))
async def hello(message: Message):
    # Создаем клавиатуру
    kb = [
        [types.KeyboardButton(text="🔮✨  Задать вопрос  ✨🔮")],
        [types.KeyboardButton(text="💳  Оформить подписку")],
        [types.KeyboardButton(text="📖 Инструкция")],
        [types.KeyboardButton(text="Личные услуги")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    
    # Отправляем сообщение с клавиатурой
    await message.answer(
        text=(
            f'Привет, {html.bold(html.quote(message.from_user.full_name))}, '
            'Я - Бот Таро, который сделает тебе расклад и ответит на все интересующие тебя вопросы 🔮\n\n'
            'Всё очень просто: напиши свой вопрос (например: "Меня любит Саша?"), выбери карты в боте и я пришлю расклад 🪄'
        ),
        reply_markup=keyboard
    )
@r.message(F.text == "Личные услуги")
async def without_puree(message: types.Message):
    await message.reply("Заказать платные индивидуальные услуги (расклады / гадание / матрица / натальные карты и т.д.) можно, перейдя в Телеграм по ссылке:"
                        "<a href='https://t.me/asi4ka2442'>@asi4ka2442</a>")
@r.message(F.text == "🔮✨  Задать вопрос  ✨🔮")
async def without_puree(message: types.Message):
    await message.reply("✨ Введите Ваш вопрос")    
    