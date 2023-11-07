from aiogram import types
from aiogram import Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.keyboards.reply import k_cancel, admin_menu
from db.dbCRUD import read_mat, create_mats, delete_mat, read_cats
from core.utils.FSM import AdminMenu

router = Router()


@router.message(F.text == 'Добавить материалы')
async def set_new_materials(msg: types.Message, state: AdminMenu.admin_main_menu):
    await msg.answer(f'Введите название категории материала, название самого материала'
                     f' и цену через косую черту, например "Стена/Бетон/1500"', reply_markup=k_cancel)
    await state.set_state(AdminMenu.adding_material)


@router.message(F.text == 'Назад')
async def back_to_main_menu(msg: types.Message, state: AdminMenu):
    await state.set_state(AdminMenu.admin_main_menu)
    await msg.answer('Вы вернулись в главное меню', reply_markup=admin_menu)


@router.message(F.text.regexp(r'[\s\S]+/\d+'))
async def adding_material(msg: types.Message, state: AdminMenu.adding_material):
    mat_category = msg.text.split('/')[0].capitalize()
    mat_name = msg.text.split('/')[1].capitalize()
    mat_price = msg.text.split('/')[2]
    create_mats(mat_category, mat_name, mat_price)
    await msg.answer(f'Материал {mat_name} добавлен. '
                     f'Можно добавить другие материалы или нажмите "Назад", чтобы выйти.', reply_markup=k_cancel)


@router.message(F.text == 'Просмотр материалов')
async def materials_lookup(msg: types.Message, state: AdminMenu.admin_main_menu):
    await msg.answer(f'Список материалов:')
    categories = read_cats()
    for cat in categories:
        await msg.answer(f'Категория: {cat[0]}')
        materials = read_mat(cat[0])
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
