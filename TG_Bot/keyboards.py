from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='За сегодня') ,KeyboardButton(text='За 3 дня')],
    [KeyboardButton(text='За 7 дней') ,KeyboardButton(text='За 14 дней')]
],
resize_keyboard=True,
    input_field_placeholder='Выберите период тех. работ'
)