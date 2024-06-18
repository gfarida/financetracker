from telegram import Update
from telegram.ext import CallbackContext
from models.finance_model import Budget, session, User

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