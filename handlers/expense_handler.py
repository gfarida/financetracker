from telegram import Update
from telegram.ext import CallbackContext
from models.finance_model import Expense, User, session
from utils.openai_util import classify_expense
import datetime


async def add_expense(update: Update, context: CallbackContext) -> None:
    try:
        args = context.args
        user_id = update.effective_user.id
        amount = float(args[0])
        description = ' '.join(args[1:])
        category = classify_expense(description)
        date = datetime.datetime.now()

        user = session.query(User).filter(User.uid == user_id).first()
        if not user:
            await update.message.reply_text('Сначала зарегистрируйтесь с помощью команды /start.')
            return

        new_expense = Expense(uid=user.uid, date=date, category=category, amount=amount)
        session.add(new_expense)
        session.commit()
        await update.message.reply_text(f'Добавлены траты: {amount} на {description} в категорию {category}')
    except Exception as e:
        print(e)
        await update.message.reply_text('Использование: /add <сумма> <описание>')


async def show_expenses(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.effective_user.id
        user = session.query(User).filter(User.uid == user_id).first()
        if not user:
            await update.message.reply_text('Сначала зарегистрируйтесь с помощью команды /start.')
            return

        expenses = session.query(Expense).filter(Expense.uid == user.uid).all()
        if not expenses:
            await update.message.reply_text('У вас пока нет трат.')
        else:
            msg = "\n".join([f"{e.date.strftime('%Y-%m-%d %H:%M:%S')}: {e.amount} на {e.category}" for e in expenses])
            await update.message.reply_text(f'Ваши траты:\n{msg}')
    except Exception as e:
        print(e)
        await update.message.reply_text('Произошла ошибка при отображении трат.')
