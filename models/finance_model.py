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
    """
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True, doc="The primary key that uniquely identifies a user.")
    name = Column(String, nullable=False, doc="The name of the user, cannot be null.")

    expenses = relationship("Expense", back_populates="user")
    budgets = relationship("Budget", back_populates="user")


class Expense(Base):
    """
    Represents an expense record in the system associated with a user.
    """
    __tablename__ = 'expenses'
    eid = Column(Integer, primary_key=True, doc="The primary key that uniquely identifies an expense.")
    uid = Column(Integer, ForeignKey('users.uid'), doc="The foreign key linked to the user who made the expense.")
    name = Column(String, doc="The name or description of the expense.")
    category = Column(String, doc="The category of the expense.")
    amount = Column(Float, doc="The amount of money spent on the expense.")
    date = Column(DateTime, doc="The date and time when the expense was recorded.")

    user = relationship("User", back_populates="expenses")


class Budget(Base):
    """
    Represents a budget set by a user for a particular category.
    """
    __tablename__ = 'budgets'
    bid = Column(Integer, primary_key=True, doc="The primary key that uniquely identifies the budget.")
    uid = Column(Integer, ForeignKey('users.uid'), doc="The foreign key linked to the user who set the budget.")
    category = Column(String, doc="The category for which the budget is set.")
    amount = Column(Float, doc="The budget amount.")

    user = relationship("User", back_populates="budgets")

engine = create_engine('sqlite:///finance_tracker.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
