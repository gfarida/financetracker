"""
This module provides functionalities to manage and record expenses for users in a Telegram bot.
It supports adding, showing, and deleting expenses. Every handler in this module requires already
registered user.

Functions:
    add_expense: Adds a new expense entry for a registered user.
    show_expenses: Displays all expenses recorded for a registered user.
    delete_expense: Deletes a specific expense entry for a registered user.
"""
import datetime

from sqlalchemy import func
from telegram import Update
from telegram.ext import CallbackContext

from models.finance_model import Expense, User, session, Budget
from utils.openai_util import classify_expense


async def add_expense(update: Update, context: CallbackContext) -> None:
    """
    Adds a new expense entry for a registered user based on their input.

    This function handles the creation of a new expense record. It automatically categorizes the
    expense based on the description provided by the user using an AI classification model.

    Args:
        update (Update): The update received from Telegram, containing the user's message and chat
                         details.
        context (CallbackContext): The context object provided by the Telegram bot framework which
                                   carries data and settings related to the command being processed.

    Raises:
        ValueError: If the amount is not a valid number or if the necessary arguments are not
                    provided.
        Exception: General exceptions that may occur during database operations or message handling.

    Usage:
        User types: /add <amount> <description>
    """
    text = update.message.text.split()

    if len(text) < 3:
        await update.message.reply_text("Please use the format: /add <amount> <description>")
        return

    try:
        args = context.args
        user_id = update.effective_user.id
        amount = float(args[0])
        description = ' '.join(args[1:])
        category = classify_expense(description)
        date = datetime.datetime.now()

        user = session.query(User).filter(User.uid == user_id).first()
        if not user:
            await update.message.reply_text('Please register first using the /start command.')
            return

        new_expense = Expense(uid=user.uid, date=date, category=category, amount=amount)
        session.add(new_expense)
        session.commit()

        # Проверка бюджета
        budget = session.query(Budget).filter_by(uid=user.uid, category=category).first()
        if not budget:
            budget = Budget(uid=user.uid, category=category, amount=float('inf'))
            session.add(budget)
            session.commit()

        total_spent = session.query(func.sum(Expense.amount)).filter_by(uid=user.uid, category=category).scalar() or 0
        if total_spent > budget.amount:
            await update.message.reply_text("Attention! Budget for category *{}* exceeded! Set budget: *{}*, current budget: *{}*".format(category, budget.amount, total_spent), parse_mode='Markdown')

        await update.message.reply_text("Expense added: {} for {} in category *{}* \nYou have spent *{:.2f}% ({}/{})* of the budget allocated for category *{}*".format(amount, description, category, (total_spent / budget.amount) * 100, total_spent, budget.amount, category), parse_mode='Markdown')

    except Exception as e:  # pylint: disable=broad-except,invalid-name
        print(e)
        await update.message.reply_text("Please use the format: /add <amount> <description>")


async def show_expenses(update: Update, context: CallbackContext) -> None:
    """
    Displays all the expenses recorded for the registered user, formatted in a readable list.

    This function fetches all the expenses associated with the user and formats them into a message
    that lists each expense with its details such as date, amount, category, and ID.

    Args:
        update (Update): The update received from Telegram, containing the user's message and chat
                         details.
        context (CallbackContext): The context object provided by the Telegram bot framework.

    Raises:
        Exception: General exceptions that may occur during data retrieval or message handling.

    Usage:
        User types: /show_expenses
    """
    try:
        user_id = update.effective_user.id
        user = session.query(User).filter(User.uid == user_id).first()
        if not user:
            await update.message.reply_text('Please register first using the /start command.')
            return

        expenses = session.query(Expense).filter(Expense.uid == user.uid).all()
        if not expenses:
            await update.message.reply_text('You have no expenses yet.')
        else:
            msg = "\n".join(["Date: *{}*, expense: *{}*, category: *{}*, ID: *{}*".format(e.date.strftime('%Y-%m-%d %H:%M:%S'), e.amount, e.category, e.eid) for e in expenses])  # pylint: disable=used-before-assignment
            await update.message.reply_text('Your expenses:\n{}'.format(msg), parse_mode='Markdown')
    except Exception as e:  # pylint: disable=broad-except,invalid-name
        print(e)
        await update.message.reply_text('An error occurred while displaying expenses.')

async def delete_expense(update: Update, context: CallbackContext):
    """
    Deletes a specific expense entry based on the ID provided by the user.

    The function checks if the expense exists under the user's account and deletes it.
    It confirms the deletion to the user by sending a success message.

    Args:
        update (Update): The update received from Telegram, containing the user's message and chat
                         details.
        context (CallbackContext): The context object provided by the Telegram bot framework.

    Raises:
        ValueError: If the expense ID is not provided or is not an integer.
        Exception: General exceptions such as database errors or if the expense does not exist.

    Usage:
        User types: /delete <expense_id>
    """
    chat_id = update.message.chat_id
    text = update.message.text.split()

    if len(text) < 2:
        await update.message.reply_text("Please use the format: /delete <expense ID>")
        return

    try:
        expense_id = int(text[1])
    except ValueError:
        await update.message.reply_text("Please enter a valid expense ID.")
        return

    user = session.query(User).filter_by(uid=chat_id).first()
    if not user:
        await update.message.reply_text("User not found.")
        return

    expense = session.query(Expense).filter_by(eid=expense_id, uid=user.uid).first()
    if not expense:
        await update.message.reply_text("Expense not found.")
        return

    session.delete(expense)
    session.commit()
    await update.message.reply_text("Expense with ID {} successfully deleted!".format(expense_id))
