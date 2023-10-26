from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel = KeyboardButton(text='Отмена')

# --- Main Menu ---
calculating = KeyboardButton(text='Расчет работ')
saved_calculating = KeyboardButton(text='Сохраненные расчеты')
main_menu = ReplyKeyboardMarkup(keyboard=[[calculating, saved_calculating]],
                                resize_keyboard=True,
                                one_time_keyboard=True)

# --- Calc Menu ---
calk_wall = KeyboardButton(text='Материал стен')
calc_cable = KeyboardButton(text='Вид кабеля')
calc_menu = ReplyKeyboardMarkup(keyboard=[[calk_wall, calc_cable], [cancel]],
                                resize_keyboard=True,
                                one_time_keyboard=True)

# --- Saved Menu ---
all_saved = KeyboardButton(text='Список сохраненных расчетов')
purge = KeyboardButton(text='Очистить')
saved_menu = ReplyKeyboardMarkup(keyboard=[[all_saved, purge], [cancel]],
                                 resize_keyboard=True,
                                 one_time_keyboard=True)


# --- Admin Menu ---
set_new_materials = KeyboardButton(text='Добавить материалы')
materials_lookup = KeyboardButton(text='Просмотр материалов')
admin_menu = ReplyKeyboardMarkup(keyboard=[[set_new_materials, materials_lookup, calculating]],
                                 resize_keyboard=True,
                                 one_time_keyboard=True)
