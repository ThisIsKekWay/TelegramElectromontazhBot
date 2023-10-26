from aiogram import types
from aiogram import Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.dbCRUD import read_saved_total, create_saved_total, delete_saved_total, read_mat
from core.utils.FSM import SavedMenu, CalcMenu, UserMenu

router = Router()


@router.message(F.text == 'Расчет работ')
async def set_new_materials(msg: types.Message, state: UserMenu.user_main_menu):
    state.set_state(CalcMenu.calc_menu)
    await msg.answer(f'Выберите материал стены:')
    walls = read_mat('Стена')
    for wall in walls:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Выбрать",
            callback_data="choose")
        )
        await msg.answer(f'Материал: {wall.name}, Цена за метр: {wall.price_for_meter} руб/м',
                         reply_markup=builder.as_markup())
        state.set_state(CalcMenu.calc_wall_type)


@router.callback_query(F.text == 'choose')
async def choose(call: types.CallbackQuery, state: CalcMenu.calc_wall_type):
    await call.answer(text=f'Выбран материал: {call.message.text}\n'
                           f'Введите применую длину штробы:')
    state.set_state(CalcMenu.calc_wall_type)
