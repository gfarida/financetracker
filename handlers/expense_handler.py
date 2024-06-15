from telegram import Update
from telegram.ext import CallbackContext
from models.finance_model import Expense, session
from utils.openai_util import classify_expense
import datetime

async def add_expense(update: Update, context: CallbackContext) -> None:
    try:
        args = context.args
        amount = float(args[0])
        description = ' '.join(args[1:])
        category = classify_expense(description)
        date = datetime.datetime.now()
        new_expense = Expense(date=date, category=category, amount=amount)
        session.add(new_expense)
        session.commit()
        await update.message.reply_text(f'Добавлены траты: {amount} на {description} в категорию {category}')
    except Exception as e:
        print(e)
        await update.message.reply_text('Использование: /add <сумма> <описание>')
