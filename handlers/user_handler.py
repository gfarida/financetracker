from telegram import Update
from telegram.ext import CallbackContext
from models.finance_model import User, session


async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    existing_user = session.query(User).filter(User.uid == user_id).first()
    
    if not existing_user:
        new_user = User(uid=user_id, name=user_name)
        session.add(new_user)
        session.commit()
        welcome_message = "Привет! Я бот для управления финансами. Вы успешно зарегистрированы."
    else:
        welcome_message = "Привет! Вы уже зарегистрированы."
    
    await update.message.reply_text(welcome_message)
