from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- Общие кнопки ---

cancel = KeyboardButton(text='Назад')
k_cancel = ReplyKeyboardMarkup(keyboard=[[cancel]], resize_keyboard=True, one_time_keyboard=True)

menu = KeyboardButton(text='В меню')
k_menu = ReplyKeyboardMarkup(keyboard=[[menu]], resize_keyboard=True, one_time_keyboard=True)


# --- Main Menu ---
calculating = KeyboardButton(text='Расчет работ')
saved_calculating = KeyboardButton(text='Сохраненное')
download_price = KeyboardButton(text='Прайс')
main_menu = ReplyKeyboardMarkup(keyboard=[[calculating, saved_calculating, download_price]],
                                resize_keyboard=True,
                                one_time_keyboard=True)

# --- Calc Menu ---
calc_under_sockets = KeyboardButton(text='Подрозетники')
calc_cable = KeyboardButton(text='Кабельные линии')
calc_strobs = KeyboardButton(text='Штробы')
calc_shields = KeyboardButton(text='Щиты')
calc_junction_boxes = KeyboardButton(text='Распред. коробки')
calc_clear_cable = KeyboardButton(text='Чистовая электрика')
calc_total = KeyboardButton(text='Итог')
calc_kb = [
    [calc_under_sockets, calc_cable, calc_strobs] ,
    [calc_shields,calc_junction_boxes, calc_clear_cable],
    [calc_total, cancel]
           ]
calc_menu = ReplyKeyboardMarkup(keyboard=calc_kb,
                                resize_keyboard=True,
                                one_time_keyboard=True,
                                row_length=3)

# --- Saved Menu ---
saved_menu = ReplyKeyboardMarkup(keyboard=[[cancel]],
                                 resize_keyboard=True,
                                 one_time_keyboard=True)


# --- Admin Menu ---
set_new_materials = KeyboardButton(text='Добавить материалы')
materials_lookup = KeyboardButton(text='Материалы')
load_file = KeyboardButton(text='Прайс')
admin_menu = ReplyKeyboardMarkup(keyboard=[[set_new_materials, materials_lookup, load_file], [calculating]],
                                 resize_keyboard=True,
                                 one_time_keyboard=True)



