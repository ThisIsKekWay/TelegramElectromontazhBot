from aiogram.fsm.state import State, StatesGroup


class CalcMenu(StatesGroup):
    calc_menu = State()
    calc_under_sockets = State()
    calc_calc_cable = State()
    calc_strobs = State()
    calc_shields1 = State()
    calc_shields2 = State()
    calc_junction_boxes = State()
    calc_cjunction_boxes = State()
    calc_ojunction_boxes = State()
    calc_clear_cable = State()
    calc_total = State()
    calc_wall_type = State()
    calc_cable_type = State()
    calc_cable_1 = State()
    calc_cable_2 = State()
    calc_cable_3 = State()
    calc_cable_4 = State()
    calc_total_cost = State()


class SavedMenu(StatesGroup):
    saved_menu = State()


class UserMenu(StatesGroup):
    user_main_menu = State()


class AdminMenu(StatesGroup):
    admin_main_menu = State()
    adding_material = State()
    saved_materials = State()
    load_price_file = State()
