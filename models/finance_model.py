from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    expenses = relationship("Expense", back_populates="user")
    budgets = relationship("Budget", back_populates="user")


class Expense(Base):
    __tablename__ = 'expenses'
    eid = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('users.uid'))
    name = Column(String)
    category = Column(String)
    amount = Column(Float)
    date = Column(DateTime)

    user = relationship("User", back_populates="expenses")


class Budget(Base):
    __tablename__ = 'budgets'
    bid = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('users.uid'))
    category = Column(String)
    amount = Column(Float)

    user = relationship("User", back_populates="budgets")


engine = create_engine('sqlite:///finance_tracker.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
