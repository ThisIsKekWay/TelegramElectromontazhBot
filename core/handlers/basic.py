from aiogram import types
from aiogram import Router
from aiogram.filters import Command
from core.keyboards.reply import main_menu, admin_menu
from aiogram.fsm.context import FSMContext
from core.utils.FSM import UserMenu, AdminMenu
import config_reader

router = Router()
ADMIN = config_reader.settings.admin_id


@router.message(Command('start'))
async def start(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    if user_id == ADMIN:
        await msg.answer(f'Привет, {msg.from_user.full_name}! Вы в главном меню.\n', reply_markup=admin_menu)
        await state.set_state(AdminMenu.admin_main_menu)
    else:
        await msg.answer(f'Привет, {msg.from_user.full_name}! Вы в главном меню.\n', reply_markup=main_menu)
        await state.set_state(UserMenu.user_main_menu)


@router.message(Command('help'))
async def main_menu_bot_help(msg: types.Message):
    await msg.answer(f'Этот бот поможет вам расчитать примерную стоимость работ по '
                     f'монтажу проводки с учетом ваших данных.\n'
                     f'Для перехода в режим расчета нажмите кнопку "Расчет".\n'
                     f'Для просмотра сохраненных вами расчетов нажмите кнопку "Сохраненные расчеты".\n')


@router.message(Command('support'))
async def support(msg: types.Message):
    await msg.answer(f'В случае возникновения ошибок и некорректной работы бота,'
                     f' пожалуйста, напишите в телеграм @Sugar_King')
