from db.model import Materials, SavedTotals, session


def create_mats(cat: str, mat_name: str, price: str):
    session.add(Materials(name=mat_name.capitalize(), price_or_coeff=price, category=cat.capitalize()))
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


def read_mat(category=None, name=None):
    if category:
        if name:
            return session.query(Materials).filter(
                Materials.category == category.capitalize(), Materials.name == name.capitalize()).all()
        else:
            return session.query(Materials).filter(
                Materials.category == category.capitalize()).all()
    else:
        if name:
            return session.query(Materials).filter(Materials.name == name.capitalize()).all()
        return session.query(Materials).all()


def create_totals(tg_id, name, total, description):
    session.add(SavedTotals(tg_id=tg_id, name=name, total_cost=total, description=description))
    session.commit()


def read_totals(tg_id):
    return session.query(SavedTotals).filter(SavedTotals.tg_id == tg_id).first()


def delete_totals(tg_id):
    session.query(SavedTotals).filter(SavedTotals.tg_id == tg_id).delete()
    session.commit()


def update_totals(tg_id, name, total, description):
    old_data = read_totals(tg_id)
    if old_data:
        total += old_data.total_cost
        description += old_data.description

        session.query(SavedTotals).filter(
            SavedTotals.tg_id == tg_id
        ).update(
            {SavedTotals.total_cost: total,
             SavedTotals.description: description})
        session.commit()
    else:
        create_totals(tg_id, name, total, description)


def final_total(tg_id):
    old_data = read_totals(tg_id)
    if old_data:
        session.query(SavedTotals).filter(
            SavedTotals.tg_id == tg_id
        ).update(
            {SavedTotals.final: True})
        session.commit()
