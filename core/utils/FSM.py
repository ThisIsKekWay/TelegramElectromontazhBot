from aiogram.fsm.state import State, StatesGroup


class CalcMenu(StatesGroup):
    calc_menu = State()
    calc_under_sockets = State()
    calc_calc_cable = State()
    calc_strobs = State()
    calc_shields = State()
    calc_junction_boxes = State()
    calc_clear_cable = State()
    calc_total = State()
    calc_wall_type = State()
    calc_cable_type = State()
    calc_total_cost = State()


class SavedMenu(StatesGroup):
    saved_menu = State()


class UserMenu(StatesGroup):
    user_main_menu = State()


class AdminMenu(StatesGroup):
    admin_main_menu = State()
    adding_material = State()
    saved_materials = State()
