from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    category = Column(String)
    amount = Column(Float)

class Budget(Base):
    __tablename__ = 'budgets'
    id = Column(Integer, primary_key=True)
    category = Column(String)
    amount = Column(Float)

engine = create_engine('sqlite:///data/database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
