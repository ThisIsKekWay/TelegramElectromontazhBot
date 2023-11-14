from aiogram import types, F
from aiogram import Router
from aiogram.filters import Command
from aiogram.utils.formatting import Bold, Text

from core.keyboards.reply import main_menu, admin_menu
from aiogram.fsm.context import FSMContext
from core.utils.FSM import UserMenu, AdminMenu
import config_reader

base_router = Router()
ADMIN = config_reader.settings.admin_id


@base_router.message(Command('start'))
async def start(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    if user_id == ADMIN:
        content = Text('Привет, ', Bold(msg.from_user.full_name), '! Вы в главном меню.\n')
        await msg.answer(**content.as_kwargs(), reply_markup=admin_menu)
        await state.set_state(AdminMenu.admin_main_menu)

    else:
        content = Text('Привет, ', Bold(msg.from_user.full_name), '! Вы в главном меню.\n',
                                                                  'Важное сообщение: \n',
                                                                  'Все расценки указаны приблизительно и не ',
                                                                  'являются офертой. Точную сумму работ вам сообщит ',
                                                                  'мастер при личной встрече и только после замеров.')
        await msg.answer(**content.as_kwargs(), reply_markup=main_menu)
        await state.set_state(UserMenu.user_main_menu)


@base_router.message(Command('help'))
async def main_menu_bot_help(msg: types.Message):
    await msg.answer(f'Этот бот поможет вам расчитать примерную стоимость работ по '
                     f'монтажу проводки с учетом ваших данных.\n'
                     f'Для перехода в режим расчета нажмите кнопку "Расчет".\n'
                     f'Для просмотра сохраненных вами расчетов нажмите кнопку "Сохраненные расчеты".\n')


@base_router.message(Command('support'))
async def support(msg: types.Message):
    await msg.answer(f'В случае возникновения ошибок и некорректной работы бота,'
                     f' пожалуйста, напишите в телеграм @Sugar_King')



