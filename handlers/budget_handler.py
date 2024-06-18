from telegram import Update
from telegram.ext import CallbackContext
from models.finance_model import Budget, session, User, Expense
from sqlalchemy import func

async def set_budget(update: Update, context: CallbackContext) -> None:
    try:
        args = context.args
        category = args[0]
        amount = float(args[1])
        user_id = update.effective_user.id  # Получаем ID пользователя
        user = session.query(User).filter(User.uid == user_id).first()

        if not user:
            await update.message.reply_text('Сначала зарегистрируйтесь с помощью команды /start.')
            return

        budget = session.query(Budget).filter_by(uid=user.uid, category=category).first()
        if budget:
            budget.amount = amount
        else:
            budget = Budget(uid=user.uid, category=category, amount=amount)
            session.add(budget)
        
        session.commit()
        await update.message.reply_text(f'Установлен бюджет: {amount} для категории {category}')
    except (IndexError, ValueError):
        await update.message.reply_text('Использование: /set_budget <категория> <сумма>')

async def delete_budget(update: Update, context: CallbackContext) -> None:
    try:
        args = context.args
        if len(args) < 1:
            await update.message.reply_text('Использование: /delete_budget <категория>')
            return

        category = args[0]
        user_id = update.effective_user.id

        budget = session.query(Budget).filter_by(uid=user_id, category=category).first()
        if budget:
            session.delete(budget)
            session.commit()
            await update.message.reply_text(f'Бюджет для категории {category} удален! Бюджет установлен в бесконечность.')
        else:
            await update.message.reply_text(f'Бюджет для категории {category} не найден.')
    except Exception as e:
        print(e)
        await update.message.reply_text('Произошла ошибка при удалении бюджета.')


async def show_budgets(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.effective_user.id

        user = session.query(User).filter(User.uid == user_id).first()
        if not user:
            await update.message.reply_text('Сначала зарегистрируйтесь с помощью команды /start.')
            return

        budgets = session.query(Budget).filter_by(uid=user_id).all()
        if not budgets:
            await update.message.reply_text('У вас нет установленных бюджетов.')
            return

        
        response = "Ваши установленные бюджеты:\n"
        for budget in budgets:
            total_spent = session.query(func.sum(Expense.amount)).filter_by(uid=user_id, category=budget.category).scalar() or 0
            response += f"Категория: *{budget.category}* - Бюджет: *{budget.amount}.* Израсходовано: *{total_spent / budget.amount * 100:.2f}% * ({total_spent} / {budget.amount})\n"

        await update.message.reply_text(response, parse_mode='Markdown')
    except Exception as e:
        print(e)
        await update.message.reply_text('Произошла ошибка при получении бюджетов.')
