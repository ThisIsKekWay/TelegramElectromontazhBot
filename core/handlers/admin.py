import os.path
import openpyxl
from aiogram import types, Bot
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.keyboards.reply import k_cancel, admin_menu
from db.dbCRUD import read_mat, create_mats, delete_mat, read_cats
from core.utils.FSM import AdminMenu


admin_router = Router()


@admin_router.message(F.text == "Назад", StateFilter(AdminMenu.adding_material, AdminMenu.saved_materials))
async def cancel(msg: types.Message, state: FSMContext):
    await msg.answer('Вы вернулись в главное меню', reply_markup=admin_menu)
    await state.set_state(AdminMenu.admin_main_menu)


@admin_router.message(F.text == 'Добавить материалы', StateFilter(AdminMenu.admin_main_menu))
async def set_new_materials(msg: types.Message, state: FSMContext):
    await msg.answer(f'Введите название категории материала, название самого материала'
                     f' и цену через косую черту, например "Стена/Бетон/1500"', reply_markup=k_cancel)
    await state.set_state(AdminMenu.adding_material)


@admin_router.message(F.text.regexp(r'[\s\S]+/\d+'), StateFilter(AdminMenu.adding_material))
async def adding_material(msg: types.document.Document, state: FSMContext):
    mat_category = msg.text.split('/')[0].capitalize()
    mat_name = msg.text.split('/')[1].capitalize()
    mat_price = msg.text.split('/')[2]
    create_mats(mat_category, mat_name, mat_price)
    await msg.answer(f'Материал {mat_name} добавлен. '
                     f'Можно добавить другие материалы или нажмите "Назад", чтобы выйти.', reply_markup=k_cancel)


@admin_router.message(F.text == 'Материалы', StateFilter(AdminMenu.admin_main_menu))
async def materials_lookup(msg: types.Message, state: FSMContext):
    await msg.answer(f'Список материалов:')
    categories = read_cats()
    for cat in categories:
        await msg.answer(f'Категория: {cat[0]}')
        materials = read_mat(category=cat[0])
        for mat in materials:
            builder = InlineKeyboardBuilder()
            builder.add(types.InlineKeyboardButton(
                text="Удалить",
                callback_data="delete_materials")
            )
            if mat.price_or_coeff < 2:
                await msg.answer(f'Имя: {str(mat.name).capitalize()}, Коэффициент: {mat.price_or_coeff}',
                                 reply_markup=builder.as_markup())
            else:
                await msg.answer(f'Имя: {str(mat.name).capitalize()}, Цена: {mat.price_or_coeff}',
                                 reply_markup=builder.as_markup())

    await state.set_state(AdminMenu.admin_main_menu)


@admin_router.callback_query(F.data == 'delete_materials', StateFilter(AdminMenu.admin_main_menu))
async def delete_materials(call: types.CallbackQuery, state: FSMContext):
    delete_mat(call.message.text.split(',')[0].split(': ')[1])
    await call.answer('Материал удален')


@admin_router.message(F.document, StateFilter(AdminMenu.admin_main_menu))
async def download_file(msg: types.Message, state: FSMContext, bot: Bot):
    file_id = msg.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    if os.path.exists('price.xlsx'):
        os.remove('price.xlsx')
        await bot.download_file(file_path, 'price.xlsx')
        await msg.answer('Файл заменен')
    else:
        await bot.download_file(file_path, 'price.xlsx')
        await msg.answer('Файл добавлен')
    await msg.answer('Обновление данных...')

    wb = openpyxl.load_workbook('price.xlsx')
    sheet = wb.active
