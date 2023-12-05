from decimal import Decimal
from aiogram import types
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot

import config_reader
from core.keyboards.reply import calc_menu, main_menu, admin_menu
from db.dbCRUD import read_mat, read_totals, delete_totals, update_totals, final_total
from core.utils.FSM import CalcMenu, UserMenu, AdminMenu

user_router = Router()
ADMIN = config_reader.settings.admin_id


@user_router.message(F.text == 'Прайс', StateFilter(UserMenu.user_main_menu, AdminMenu.admin_main_menu))
async def download_price(msg: types.Message, state: FSMContext):
    price = types.FSInputFile("price.xlsx")
    await msg.answer_document(price)


@user_router.message(F.text == 'Назад', StateFilter(CalcMenu.calc_calc_cable, CalcMenu.calc_under_sockets,
                                                    CalcMenu.calc_strobs, CalcMenu.calc_shields1,
                                                    CalcMenu.calc_junction_boxes, CalcMenu.calc_clear_cable,
                                                    CalcMenu.calc_total, CalcMenu.calc_wall_type,
                                                    CalcMenu.calc_cable_type, CalcMenu.calc_total_cost,
                                                    CalcMenu.calc_menu, CalcMenu.calc_shields2)
                     )
async def back(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    if user_id == ADMIN:
        await state.set_state(AdminMenu.admin_main_menu)
        await msg.answer('Вы в главном меню', reply_markup=admin_menu)
    else:
        await state.set_state(UserMenu.user_main_menu)
        await msg.answer('Вы в главном меню', reply_markup=main_menu)


@user_router.message(F.text == 'Расчет работ', StateFilter(UserMenu.user_main_menu, AdminMenu.admin_main_menu))
async def set_new_materials(msg: types.Message, state: FSMContext):
    await state.set_state(CalcMenu.calc_menu)
    await msg.answer('Выберите категорию', reply_markup=calc_menu)


@user_router.message(F.text.in_({'Подрозетники', 'Штробы'}), StateFilter(CalcMenu.calc_menu))
async def under_sockets(msg: types.Message, state: FSMContext):
    await state.set_state(CalcMenu.calc_under_sockets)
    if msg.text == 'Подрозетники':
        await msg.answer('В какую стену нужно устанавливать подрозетники?\nПерешлите сообщение с числом подрозетников:')
        await state.set_state(CalcMenu.calc_under_sockets)
    if msg.text == 'Штробы':
        await msg.answer('В какую стену нужно устанавливать шробы?\nПерешлите сообщение с числом штроб:')
        await state.set_state(CalcMenu.calc_strobs)
    walls = read_mat('Стена')
    for wall in walls:
        await msg.answer(f'{wall.name}, Коэффициент: {wall.price_or_coeff}')


@user_router.message(F.text.in_({'ok', 'ок', 'Ок', 'Ok', 'OK'}), StateFilter(CalcMenu.calc_calc_cable,
                                                                             CalcMenu.calc_under_sockets,
                                                                             CalcMenu.calc_strobs,
                                                                             CalcMenu.calc_shields1,
                                                                             CalcMenu.calc_junction_boxes,
                                                                             CalcMenu.calc_ojunction_boxes,
                                                                             CalcMenu.calc_cjunction_boxes,
                                                                             CalcMenu.calc_clear_cable,
                                                                             CalcMenu.calc_total,
                                                                             CalcMenu.calc_wall_type,
                                                                             CalcMenu.calc_cable_type,
                                                                             CalcMenu.calc_total_cost,
                                                                             CalcMenu.calc_shields2,
                                                                             CalcMenu.calc_cable_1,
                                                                             CalcMenu.calc_cable_2,
                                                                             CalcMenu.calc_cable_3,
                                                                             CalcMenu.calc_cable_4, ))
async def menu(msg: types.Message, state: FSMContext):
    await msg.answer('Вы в меню расчета', reply_markup=calc_menu)
    await state.set_state(CalcMenu.calc_menu)


@user_router.message(StateFilter(CalcMenu.calc_under_sockets,
                                 CalcMenu.calc_strobs,
                                 CalcMenu.calc_cjunction_boxes,
                                 CalcMenu.calc_cable_type,
                                 CalcMenu.calc_cable_1,
                                 CalcMenu.calc_cable_2,
                                 CalcMenu.calc_cable_3,
                                 CalcMenu.calc_cable_4, ))
async def forward_under_sockets(msg: types.Message, state: FSMContext):
    state_dict = {
        CalcMenu.calc_cable_1: 'Пучок',
        CalcMenu.calc_cable_2: 'Отдельный',
        CalcMenu.calc_cable_3: 'Гофра',
        CalcMenu.calc_cable_4: 'Канал'
    }
    if msg.reply_to_message:
        description = ''
        cur_state = await state.get_state()
        wall = msg.reply_to_message.text.split(', Коэффициент: ')
        name = msg.from_user.full_name
        id = msg.from_user.id
        wall_type = wall[0]
        wall_price = Decimal(wall[1])
        try:
            prod_count = int(msg.text)
        except Exception as e:
            print(e)
            await msg.answer('Некорректное значение. Повторите попытку.')
            return
        if cur_state == CalcMenu.calc_under_sockets:
            prod = read_mat(name='Подрозетник')[0]
            prod_price = Decimal(prod.price_or_coeff)
            units = 'шт.'
        elif cur_state == CalcMenu.calc_strobs:
            units = 'м.'
            prod = read_mat(name='Штроба')[0]
            prod_price = Decimal(prod.price_or_coeff)
        elif cur_state == CalcMenu.calc_cjunction_boxes:
            units = 'шт.'
            prod = read_mat(name='Распред.короб')[0]
            prod_price = Decimal(prod.price_or_coeff)
        elif cur_state in state_dict:
            description = 'Кабель в '
            units = 'м.'
            prod = read_mat(name=state_dict[cur_state])[0]
            prod_price = Decimal(prod.price_or_coeff)
        total = prod_count * wall_price * prod_price
        description += f'{prod.name} в {wall_type}: {prod_count} {units} = {total.quantize(2)} руб.\n'
        update_totals(id, name, total, description)
        await msg.answer('Данные добавлены, вы можете дополнить их сейчас или позже.\n'
                         'Для возврата в меню напишите боту "ок"')
    else:
        await msg.answer('Некорректная команда. Повторите попытку.')


@user_router.message(F.text.in_({'Итог', 'Сохраненное'}), StateFilter(CalcMenu.calc_menu, UserMenu.user_main_menu))
async def itog(msg: types.Message, state: FSMContext):
    total = read_totals(msg.from_user.id)
    if total:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Удалить",
            callback_data="delete_totals")
        )
        cur_state = await state.get_state()
        print(cur_state)
        if cur_state == UserMenu.user_main_menu:
            builder.add(types.InlineKeyboardButton(
                text="Отправить мастеру",
                callback_data="send_to_master")
            )
        elif cur_state == CalcMenu.calc_menu:
            builder.add(types.InlineKeyboardButton(
                text="Сохранить",
                callback_data="save")
            )

        res = total.description + '______________________________\n' + f'Итого: {total.total_cost.quantize(2)} руб.'
        await msg.answer(res, reply_markup=builder.as_markup())
    else:
        await msg.answer('Сохраненных расчетов нет')


@user_router.callback_query(F.data == 'delete_totals', StateFilter(CalcMenu.calc_menu, UserMenu.user_main_menu))
async def delete_materials(call: types.CallbackQuery, state: FSMContext):
    delete_totals(call.from_user.id)
    await call.answer('Расчет удален')


@user_router.callback_query(F.data == 'send_to_master', StateFilter(UserMenu.user_main_menu))
async def send_to_master(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    if not call.from_user.username:
        await bot.send_message(call.from_user.id, 'У вас не задан username.'
                                                  'Пожалуйста, укажите его в настройках Telegram'
                                                  'или укажите свой номер телефона в ответном сообщении')
        return
    total = read_totals(call.from_user.id)
    if total:
        await bot.send_message(ADMIN, f'Заказ от https://t.me/{call.from_user.username}:\n{total.description}')
        delete_totals(call.from_user.id)
        await call.answer('Заказ отправлен, мастер скоро свяжется с вами')


@user_router.callback_query(F.data == 'save', StateFilter(CalcMenu.calc_menu))
async def save_total(call: types.CallbackQuery, state: FSMContext):
    total = read_totals(call.from_user.id)
    if total:
        final_total(call.from_user.id)
        await call.answer('Расчет завершен. Вы можете отправить его мастеру через главное меню. '
                          'После отправки вы начнете новый расчет.')
    else:
        await call.answer('Сохранять нечего')


@user_router.message(F.text == 'Чистовая электрика', StateFilter(CalcMenu.calc_menu))
async def clear_cable(msg: types.Message, state: FSMContext):
    await state.set_state(CalcMenu.calc_clear_cable)
    await msg.answer('Перешлите это сообщение с необходимым числом')


@user_router.message(StateFilter(CalcMenu.calc_clear_cable))
async def forward_under_sockets(msg: types.Message, state: FSMContext):
    if msg.reply_to_message:
        name = msg.from_user.full_name
        id = msg.from_user.id
        try:
            prod_count = int(msg.text)
        except Exception as e:
            print(e)
            await msg.answer('Некорректное значение. Повторите попытку.')
            return
        prod_price = Decimal(read_mat(name='Чистовая электрика')[0].price_or_coeff)
        total = prod_count * prod_price
        description = f'Чистовая электрика: {prod_count} шт. = {total.quantize(2)} руб.\n'
        update_totals(id, name, total, description)
        await msg.answer('Данные добавлены, вы можете дополнить их сейчас или позже.\n'
                         'Для возврата в меню напишите боту "ок"')
    else:
        await msg.answer('Некорректная команда. Повторите попытку.')


@user_router.message(F.text.in_({"Щиты", "Распред. коробки"}), StateFilter(CalcMenu.calc_menu))
async def shields(msg: types.Message, state: FSMContext):
    if msg.text == 'Щиты':
        await state.set_state(CalcMenu.calc_shields1)
    if msg.text == 'Распред. коробки':
        await state.set_state(CalcMenu.calc_junction_boxes)
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="Открытый",
            callback_data="Open"),
        types.InlineKeyboardButton(
            text="Скрытый",
            callback_data="Closed")
    )
    await msg.answer('Выберите метод установки', reply_markup=builder.as_markup())


@user_router.callback_query(F.data == 'Closed', StateFilter(CalcMenu.calc_shields1, CalcMenu.calc_junction_boxes))
async def closed_shields(call: types.CallbackQuery, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state == CalcMenu.calc_shields1:
        await state.set_state(CalcMenu.calc_shields2)
        await call.message.answer('Выберите стену для внутренней установки\n'
                                  'Перешлите сообщение с предполагаемым числом модулей щита.'
                                  '12, 24, 36, 48')
    if cur_state == CalcMenu.calc_junction_boxes:
        await state.set_state(CalcMenu.calc_cjunction_boxes)
        await call.message.answer('Выберите стену для внутренней установки\n'
                                  'Перешлите сообщение с числом коробок.')
    walls = read_mat(category='Стена')
    for wall in walls:
        await call.message.answer(f'{wall.name}, Коэффициент: {wall.price_or_coeff}')


@user_router.message(StateFilter(CalcMenu.calc_shields2))
async def forward_shields(msg: types.Message, state: FSMContext):
    if msg.reply_to_message:
        wall = msg.reply_to_message.text.split(', Коэффициент: ')
        name = msg.from_user.full_name
        id = msg.from_user.id
        wall_type = wall[0]
        wall_price = Decimal(wall[1])
        try:
            shield_mods = int(msg.text)
            if shield_mods not in [12, 24, 36, 48]:
                await msg.answer('Некорректное значение. Повторите попытку.')
                return
        except Exception as e:
            print(e)
            await msg.answer('Некорректное значение. Повторите попытку.')
            return
        shield = read_mat(name=f'Щит {shield_mods} мод')[0]
        prod_price = Decimal(shield.price_or_coeff)
        total = prod_price * wall_price
        description = f'{shield.name} в {wall_type} = {total.quantize(2)} руб.\n'
        update_totals(id, name, total, description)
        await msg.answer('Данные добавлены, вы можете дополнить их сейчас или позже.\n'
                         'Для возврата в меню напишите боту "ок"')
    else:
        await msg.answer('Некорректная команда. Повторите попытку.')


@user_router.callback_query(F.data == 'Open', StateFilter(CalcMenu.calc_shields1,
                                                          CalcMenu.calc_junction_boxes))
async def open_shield(call: types.CallbackQuery, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state == CalcMenu.calc_shields1:
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(
                text="12 мод",
                callback_data="12"),
            types.InlineKeyboardButton(
                text="24 мод",
                callback_data="24"),
            types.InlineKeyboardButton(
                text="36 мод",
                callback_data="36"),
            types.InlineKeyboardButton(
                text="48 мод",
                callback_data="48")
        )
        await call.message.answer('Выберите предполагаемое количество модулей щита.',
                                  reply_markup=builder.as_markup())
    if cur_state == CalcMenu.calc_junction_boxes:
        await state.set_state(CalcMenu.calc_ojunction_boxes)
        await call.message.answer('Введите в ответе предполагаемое количество коробок.')


@user_router.callback_query(F.data.in_(['12', '24', '36', '48']), StateFilter(CalcMenu.calc_shields1))
async def open_shield2(call: types.CallbackQuery, state: FSMContext):
    name = call.from_user.full_name
    id = call.from_user.id
    shield = read_mat(name=f'Щит {call.data} мод')[0]
    prod_price = Decimal(shield.price_or_coeff)
    total = prod_price
    description = f'Открытый {shield.name} = {total.quantize(2)} руб.\n'
    update_totals(id, name, total, description)
    await call.message.answer('Данные добавлены, вы можете дополнить их сейчас или позже.\n'
                              'Для возврата в меню напишите боту "ок"')


@user_router.message(F.text == 'Кабельные линии', StateFilter(CalcMenu.calc_menu))
async def cable_lines(msg: types.Message, state: FSMContext):
    await state.set_state(CalcMenu.calc_cable_type)
    builder = InlineKeyboardBuilder()
    cabels = read_mat(category='Кабель')
    for cabel in cabels:
        builder.add(
            types.InlineKeyboardButton(
                text=f'{cabel.name}',
                callback_data=f'{cabel.name}')
        )
    await msg.answer('Выберите способ прокладки кабеля\n', reply_markup=builder.as_markup())


@user_router.callback_query(F.data.in_(['Пучок', 'Отдельный', 'Гофра', 'Канал']),
                            StateFilter(CalcMenu.calc_cable_type))
async def cable_lines2(call: types.CallbackQuery, state: FSMContext):
    state_dict = {
        'Пучок': CalcMenu.calc_cable_1,
        'Отдельный': CalcMenu.calc_cable_2,
        'Гофра': CalcMenu.calc_cable_3,
        'Канал': CalcMenu.calc_cable_4
    }
    await call.message.answer('Выберите тип стены для прокладки кабеля.\n'
                              'Перешлите сообщение с предполагаемой длиной кабеля.')
    walls = read_mat(category='Стена')
    for wall in walls:
        await call.message.answer(f'{wall.name}, Коэффициент: {wall.price_or_coeff}')
    await state.set_state(state_dict[call.data])


@user_router.message(StateFilter(CalcMenu.calc_ojunction_boxes))
async def forward_junk(msg: types.Message, state: FSMContext):
    if msg.reply_to_message:
        name = msg.from_user.full_name
        id = msg.from_user.id
        try:
            prod_count = int(msg.text)
        except Exception as e:
            print(e)
            await msg.answer('Некорректное значение. Повторите попытку.')
            return
        prod_price = Decimal(read_mat(name='Распред.короб')[0].price_or_coeff)
        total = prod_count * prod_price
        description = f'Открытый распред.короб: {prod_count} шт. = {total.quantize(2)} руб.\n'
        update_totals(id, name, total, description)
        await msg.answer('Данные добавлены, вы можете дополнить их сейчас или позже.\n'
                         'Для возврата в меню напишите боту "ок"')
    else:
        await msg.answer('Некорректная команда. Повторите попытку.')
