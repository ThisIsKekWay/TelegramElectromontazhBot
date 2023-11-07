from aiogram import types
from aiogram import Router, F

from core.keyboards.reply import calc_menu
from db.dbCRUD import read_saved_total, create_saved_total, delete_saved_total, read_mat, read_cats
from core.utils.FSM import SavedMenu, CalcMenu, UserMenu

router = Router()


@router.message(F.text == 'Расчет работ')
async def set_new_materials(msg: types.Message, state: UserMenu.user_main_menu):
    state.set_state(CalcMenu.calc_menu)
    await msg.answer('Выберите категорию', reply_markup=calc_menu)


@router.message(F.text == 'Подрозетники')
async def under_sockets(msg: types.Message, state: CalcMenu.calc_menu):
    state.set_state(CalcMenu.calc_under_sockets)
    await msg.answer('Ответьте на сообщение числом подрозетников:')
    walls = read_mat('Стена')
    for wall in walls:
        await msg.answer(f'{wall.name} - {wall.price_for_meter} руб.')


@router.message()
async def forward_under_sockets(msg: types.Message, state: CalcMenu.calc_under_sockets):
    wall = msg.reply_to_message.text[:-5].split(' - ')
    wall_type = wall[0]
    wall_price = wall[1]
    prod_count = int(msg.text)
    print(wall_type)
