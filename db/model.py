from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, DECIMAL
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine("sqlite:///materials.db", echo=True)


class Base(DeclarativeBase):
    pass


class Materials(Base):
    __tablename__ = 'materials'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False)
    price_for_meter = Column(Integer, nullable=False)
    visible = Column(Boolean, default=True)


class SavedTotals(Base):
    __tablename__ = 'saved_totals'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False, unique=True)
    total_cost = Column(Integer, nullable=False)
    visible = Column(Boolean, default=True)


class CalkingProcess(Base):
    __tablename__ = 'calking_process'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, nullable=False)
    description = Column(Text, nullable=False, unique=False)
    under_sockets = Column(DECIMAL, nullable=True)
    calc_cable = Column(DECIMAL, nullable=True)
    strobs = Column(DECIMAL, nullable=True)
    shields = Column(DECIMAL, nullable=True)
    junction_boxes = Column(DECIMAL, nullable=True)
    clear_cable = Column(DECIMAL, nullable=True)
    total_cost = Column(DECIMAL, nullable=True)


Session = sessionmaker(bind=engine)
session = Session()


def create_db():
    if not os.path.exists('materials.db'):
        Base.metadata.create_all(engine)
        return True
    else:
        return False
