from aiogram import types
from aiogram import Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.dbCRUD import read_mat, create_mats, delete_mat
from core.utils.FSM import AdminMenu


router = Router()


@router.message(F.text == 'Добавить материалы')
async def set_new_materials(msg: types.Message, state: AdminMenu.admin_main_menu):
    await msg.answer(f'Введите название категории материала, название самого материала'
                     f' и цену через косую черту, например "Стена/Бетон/1500"')
    await state.set_state(AdminMenu.adding_material)


@router.message(F.text.regexp(r'[\s\S]+/\d+'))
async def adding_material(msg: types.Message, state: AdminMenu.adding_material):
    if msg.text == 'ок':
        await msg.answer('Выход из добавления')
        await state.set_state(AdminMenu.admin_main_menu)
    else:
        mat_category = msg.text.split('/')[0]
        mat_name = msg.text.split('/')[1]
        mat_price = msg.text.split('/')[2]
        create_mats(mat_category, mat_name, mat_price)
        await msg.answer(f'Материал {mat_name} добавлен. '
                         f'Можно добавить другие материалы или введите "ок", чтобы выйти.')


@router.message(F.text == 'Просмотр материалов')
async def materials_lookup(msg: types.Message, state: AdminMenu.admin_main_menu):
    await msg.answer(f'Список материалов:')
    materials = read_mat()
    for mat in materials:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Удалить",
            callback_data="delete_materials")
            )
        await msg.answer(f'Имя: {str(mat.name).capitalize()}, Цена: {mat.price_for_meter}',
                         reply_markup=builder.as_markup())

    await state.set_state(AdminMenu.saved_materials)


@router.callback_query(F.data == 'delete_materials')
async def delete_materials(call: types.CallbackQuery, state: AdminMenu.saved_materials):
    delete_mat(call.message.text.split(',')[0].split(': ')[1])
    await call.answer('Материал удален')
    await state.set_state(AdminMenu.admin_main_menu)
