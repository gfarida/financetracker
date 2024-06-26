"""
This module provides handlers for managing budgets and performing financial analysis in a Telegram
bot. The handlers include setting a budget, deleting a budget, showing all budgets, and conducting
financial analysis over a specified period. Every handler in this module requires already registered
user.

Functions:
    set_budget: Sets a budget for a specific category.
    delete_budget: Deletes a budget for a specific category.
    show_budgets: Shows all budgets and their statuses.
    financial_analysis: Provides financial analysis for a specified period.
"""

import datetime

from telegram import Update
from telegram.ext import CallbackContext
from sqlalchemy import func
import plotly.graph_objects as go


from models.finance_model import Budget, session, User, Expense


async def set_budget(update: Update, context: CallbackContext) -> None:
    """
    Sets a budget for a specific category for the registered user.

    Args:
        update (telegram.Update): Incoming update from the user.
        context (telegram.ext.CallbackContext): Context object passed from the handler.

    Usage:
        /set_budget <category> <amount>
    """
    try:
        args = context.args
        category = args[0]
        amount = float(args[1])
        user_id = update.effective_user.id  # Получаем ID пользователя
        user = session.query(User).filter(User.uid == user_id).first()

        if not user:
            await update.message.reply_text('Please register first using the /start command.')
            return

        budget = session.query(Budget).filter_by(uid=user.uid, category=category).first()
        if budget:
            budget.amount = amount
        else:
            budget = Budget(uid=user.uid, category=category, amount=amount)
            session.add(budget)

        session.commit()
        await update.message.reply_text('Budget set: {} for category {}'.format(amount, category))
    except (IndexError, ValueError):
        await update.message.reply_text('Usage: /set_budget <category> <amount>')


async def delete_budget(update: Update, context: CallbackContext) -> None:
    """
    Deletes a budget for a specific category for the registered user.

    Args:
        update (telegram.Update): Incoming update from the user.
        context (telegram.ext.CallbackContext): Context object passed from the handler.

    Usage:
        /delete_budget <category>
    """
    try:
        args = context.args
        if len(args) < 1:
            await update.message.reply_text('Usage: /delete_budget <category>')
            return

        category = args[0]
        user_id = update.effective_user.id

        budget = session.query(Budget).filter_by(uid=user_id, category=category).first()
        if budget:
            session.delete(budget)
            session.commit()
            await update.message.reply_text('Budget for category {} deleted! Budget set to infinity.'.format(category))
        else:
            await update.message.reply_text('Budget for category {} not found.'.format(category))
    except Exception as e:  # pylint: disable=broad-except,invalid-name
        print(e)
        await update.message.reply_text('An error occurred while deleting the budget.')


async def show_budgets(update: Update, context: CallbackContext) -> None:
    """
    Shows all budgets set by the registered user along with the spending status for each budget.

    Args:
        update (telegram.Update): Incoming update from the user.
        context (telegram.ext.CallbackContext): Context object passed from the handler.

    Usage:
        /show_budgets
    """
    try:
        user_id = update.effective_user.id

        user = session.query(User).filter(User.uid == user_id).first()
        if not user:
            await update.message.reply_text('Please register first using the /start command.')
            return

        budgets = session.query(Budget).filter_by(uid=user_id).all()
        if not budgets:
            await update.message.reply_text('You have no set budgets.')
            return

        response = "Your set budgets:\n"
        for budget in budgets:
            total_spent = session.query(func.sum(Expense.amount)).filter_by(uid=user_id, category=budget.category).scalar() or 0
            response += "Category: *{}* - Budget: *{}.* Spent: *{:.2f}% * ({} / {})\n".format(budget.category, budget.amount, total_spent / budget.amount * 100, total_spent, budget.amount)

        await update.message.reply_text(response, parse_mode='Markdown')
    except Exception as e:  # pylint: disable=broad-except,invalid-name
        print(e)
        await update.message.reply_text('An error occurred while retrieving budgets.')


async def financial_analysis(update: Update, context: CallbackContext) -> None:
    """
    Provides financial analysis for a specified period for the registered user.

    Args:
        update (telegram.Update): Incoming update from the user.
        context (telegram.ext.CallbackContext): Context object passed from the handler.

    Usage:
        /financial_analysis <start_date> <start_time> <end_date> <end_time>
        Date and time format: YYYY-MM-DD HH:MM:SS
    """
    try:
        args = context.args
        start_date_str = args[0]
        start_time_str = args[1]
        end_date_str = args[2]
        end_time_str = args[3]

        start_datetime = datetime.datetime.strptime(start_date_str + ' ' + start_time_str,
                                                    '%Y-%m-%d %H:%M:%S')
        end_datetime = datetime.datetime.strptime(end_date_str + ' ' + end_time_str,
                                                  '%Y-%m-%d %H:%M:%S')

        user_id = update.effective_user.id

        expenses = session.query(Expense).filter(
            Expense.uid == user_id,
            Expense.date >= start_datetime,
            Expense.date <= end_datetime
        ).all()

        total_expenses = sum(expense.amount for expense in expenses)

        categories = set(expense.category for expense in expenses)
        category_expenses = {
            category: sum(expense.amount for expense in expenses if expense.category == category)
            for category in categories
        }

        if total_expenses == 0:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="There are no expenses for the current period")
            return
        response = "Financial analysis from *{} {}* to *{} {}*:\n".format(start_date_str, start_time_str, end_date_str, end_time_str)
        response += "*Total expenses*: {}\n\n".format(total_expenses)
        response += "Expenses by category:\n"
        for category, amount in category_expenses.items():
            response += f"*{category}*: {amount}\n"

        labels = list(category_expenses.keys())
        sizes = list(category_expenses.values())

        fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, textinfo='label+percent',
                                    texttemplate='%{label} (%{percent:.2%})', insidetextorientation='radial', hole=.3)])

        fig.update_layout(title_text='Expenses by category')
        pie_chart_path = 'pie_chart.png'
        fig.write_image(pie_chart_path, scale=1.5)


        await context.bot.send_photo(chat_id=update.effective_chat.id,
                                     photo=open(pie_chart_path,'rb'),
                                     caption=response, parse_mode='Markdown')

    except IndexError:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Please use the format: /financial_analysis <start_date> <start_time> <end_date> <end_time>. Date and time format: YYYY-MM-DD HH:MM:SS')
    except Exception as e:  # pylint: disable=broad-except,invalid-name
        print(e)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='An error occurred during the analysis.')
