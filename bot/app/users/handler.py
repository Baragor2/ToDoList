from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.users.auth import login_user, register_user
from app.users.keyboards import main_keyboard
from app.users.states import Registration

router = Router()


@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    tg_id = str(message.from_user.id)

    response = await login_user(tg_id)
    if response.json() == {'message': 'successful login'}:
        await message.answer("Добро пожаловать! Выберите действие:", reply_markup=main_keyboard)
    else:
        await message.answer("Добро пожаловать! Для регистрации введите имя:")
        await state.set_state(Registration.waiting_for_name)


@router.message(Registration.waiting_for_name)
async def name_received(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Теперь введите email:")
    await state.set_state(Registration.waiting_for_email)


@router.message(Registration.waiting_for_email)
async def name_received(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Теперь введите пароль:")
    await state.set_state(Registration.waiting_for_password)


@router.message(Registration.waiting_for_password)
async def password_received(message: Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data.get("name")
    email = user_data.get("email")
    password = message.text

    response = await register_user(str(message.from_user.id), name, email, password)
    if response.json() == {"message": "successful telegram integration"}:
        await message.answer("Интеграция с телеграм успешна! Выберите действие:", reply_markup=main_keyboard)
    elif response.json() == {"message": "successful registration"}:
        await message.answer("Регистрация успешна! Выберите действие:", reply_markup=main_keyboard)
    else:
        await message.answer("Регистрация не удалась!")
    await state.clear()
