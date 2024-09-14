from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_keyboard_buttons = [
    [KeyboardButton(text="Просмотреть задачи"), KeyboardButton(text="Создать задачу")],
    [KeyboardButton(text="Просмотреть комментарии"), KeyboardButton(text="Создать комментарий")],
]
main_keyboard = ReplyKeyboardMarkup(
    keyboard=main_keyboard_buttons,
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)

