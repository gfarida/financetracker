from telegram import Update
from telegram.ext import CallbackContext
from models.finance_model import Expense, User, session, Budget
from utils.openai_util import classify_expense
import datetime
from sqlalchemy import func


async def add_expense(update: Update, context: CallbackContext) -> None:
    text = update.message.text.split()

    if len(text) < 3:
        await update.message.reply_text("Пожалуйста, используйте формат: /add <сумма> <описание>")
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
            await update.message.reply_text('Сначала зарегистрируйтесь с помощью команды /start.')
            return

        new_expense = Expense(uid=user.uid, date=date, category=category, amount=amount)
        session.add(new_expense)
        session.commit()

        print(f"User ID: {user.uid}, Category: {category}")

        # Проверка бюджета
        budget = session.query(Budget).filter_by(uid=user.uid, category=category).first()
        print(budget)
        if budget:
            total_spent = session.query(Expense).filter_by(uid=user.uid, category=category).with_entities(func.sum(Expense.amount)).scalar() or 0
            if total_spent > budget.amount:
                await update.message.reply_text(f"Внимание! Бюджет для категории *{category}* превышен! Установленный бюджет: *{budget.amount}*, текущий бюджет: *{total_spent}*", parse_mode='Markdown')

        await update.message.reply_text(f"Трата добавлена! Трата: *{amount}*, название: *{description}*, категория: *{category}* \n"
                                        f"Вы израсходовали *{(total_spent / budget.amount) * 100:.2f}%* бюджета, выделенного на категорию *{category}*", parse_mode='Markdown')
    except Exception as e:
        print(e)
        await update.message.reply_text("Пожалуйста, используйте формат: /add <сумма> <описание>")


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
            msg = "\n".join([f"Дата: *{e.date.strftime('%Y-%m-%d %H:%M:%S')}*, трата: *{e.amount}*, категория: *{e.category}*, ID: *{e.eid}*" for e in expenses])
            await update.message.reply_text(f'Ваши траты:\n{msg}', parse_mode='Markdown')
    except Exception as e:
        print(e)
        await update.message.reply_text('Произошла ошибка при отображении трат.')

async def delete_expense(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text.split()
    
    if len(text) < 2:
        await update.message.reply_text("Пожалуйста, используйте формат: /delete <id траты>")
        return

    try:
        expense_id = int(text[1])
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите правильный ID траты.")
        return

    user = session.query(User).filter_by(uid=chat_id).first()
    if not user:
        await update.message.reply_text("Пользователь не найден.")
        return

    expense = session.query(Expense).filter_by(eid=expense_id, uid=user.uid).first()
    if not expense:
        await update.message.reply_text("Трата не найдена.")
        return

    session.delete(expense)
    session.commit()
    await update.message.reply_text(f"Трата с ID {expense_id} успешно удалена!")