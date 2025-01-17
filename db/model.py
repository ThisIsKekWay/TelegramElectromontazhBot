from sqlalchemy import create_engine, Column, Integer, String, Text, Numeric, Boolean
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
    price_or_coeff = Column(Numeric(precision=9, scale=2), nullable=False)


class SavedTotals(Base):
    __tablename__ = 'saved_totals'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False, unique=True)
    total_cost = Column(Numeric(precision=9, scale=2), nullable=False)
    description = Column(Text, nullable=True)
    final = Column(Boolean, nullable=False, default=False)


Session = sessionmaker(bind=engine)
session = Session()


def create_db():
    if not os.path.exists('materials.db'):
        Base.metadata.create_all(engine)
        return True
    else:
        return False
