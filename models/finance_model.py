"""
This module defines the database schema using SQLAlchemy ORM for a finance tracking system.

Users represent individual accounts, Expenses record financial transactions of these users,
and Budgets set spending limits for categorized expenses. One user may have any number of
expenses and budgets.

The module sets up a SQLite database engine, creates all necessary tables based on the model
definitions, and establishes a session for interacting with the database.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()


class User(Base):
    """
    Represents a user in the system with related expenses and budgets.

    Attributes:
        uid (int): The primary key that uniquely identifies a user.
        name (str): The name of the user, cannot be null.
        expenses (relationship): A list of Expense instances associated with the user.
        budgets (relationship): A list of Budget instances associated with the user.
    """
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    expenses = relationship("Expense", back_populates="user")
    budgets = relationship("Budget", back_populates="user")


class Expense(Base):
    """
    Represents an expense record in the system associated with a user.

    Attributes:
        eid (int): The primary key that uniquely identifies an expense.
        uid (int): The foreign key linked to the user who made the expense.
        name (str): The name or description of the expense.
        category (str): The category of the expense.
        amount (float): The amount of money spent on the expense.
        date (DateTime): The date and time when the expense was recorded.
        user (relationship): The User instance this expense is associated with.
    """
    __tablename__ = 'expenses'
    eid = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('users.uid'))
    name = Column(String)
    category = Column(String)
    amount = Column(Float)
    date = Column(DateTime)

    user = relationship("User", back_populates="expenses")


class Budget(Base):
    """
    Represents a budget set by a user for a particular category.

    Attributes:
        bid (int): The primary key that uniquely identifies the budget.
        uid (int): The foreign key linked to the user who set the budget.
        category (str): The category for which the budget is set.
        amount (float): The budget amount.
        user (relationship): The User instance this budget is associated with.
    """
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
