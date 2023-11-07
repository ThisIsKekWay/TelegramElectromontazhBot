from db.model import Materials, SavedTotals, session


def create_mats(cat: str, mat_name: str, price: str):
    session.add(Materials(name=mat_name.capitalize(), price_for_meter=price, category=cat.capitalize()))
    session.commit()
    return f'Материал {mat_name} добавлен'


def delete_mat(mat_name):
    session.query(Materials).filter(
        Materials.name == mat_name.capitalize()).delete()
    session.commit()
    return f'Материал {mat_name} удален'


def search_mat(mat_name):
    return session.query(Materials).filter(
        Materials.name == mat_name.lower()).all()


def read_cats():
    return session.query(Materials.category).distinct().all()


def read_mat(category=None):
    if category:
        return session.query(Materials).filter(
            Materials.category == category).all()
    else:
        return session.query(Materials).all()


def create_saved_total(total_name, total_cost):
    session.add(SavedTotals(name=total_name.lower(), total_cost=total_cost))
    session.commit()
    return f'Сохраненный расчет {total_name} добавлен'


def delete_saved_total(total_name, tg_id):
    session.query(SavedTotals).filter(
        SavedTotals.tg_id == tg_id,
        SavedTotals.name == total_name.lower(),
        SavedTotals.visible is True).delete()
    session.commit()
    return f'Сохраненный расчет {total_name} удален'


def read_saved_total(total_name):
    return session.query(SavedTotals).filter(
        SavedTotals.name == total_name,
        SavedTotals.visible is True).all()
