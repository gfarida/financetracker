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
        welcome_message = ("Привет! Я бот для управления финансами. Вы успешно зарегистрированы.\n"
                            "Доступные команды:\n"
                            "/start - Зарегистрироваться\n"
                            "/add <сумма> <описание> - Добавить трату\n"
                            "/set_budget <категория> <сумма> - Установить бюджет для категории\n"
                            "/delete_budget <категория> - Удалить установленный бюджет для категории\n"
                            "/show_budgets - Показать все установленные бюджеты\n"
                            "/show - Показать все добавленные траты\n"
                            "/remove_expense <id> - Удалить трату по ID\n"
                            "/analysis <start_date> <start_time> <end_date> <end_time>. Формат даты и времени: YYYY-MM-DD HH:MM:SS\n"
                            "/help - Показать это сообщение\n")
    else:
        welcome_message = ("Привет! Вы уже зарегистрированы.\n"
                            "Доступные команды:\n"
                            "/start - Зарегистрироваться\n"
                            "/add <сумма> <описание> - Добавить трату\n"
                            "/set_budget <категория> <сумма> - Установить бюджет для категории\n"
                            "/delete_budget <категория> - Удалить установленный бюджет для категории\n"
                            "/show_budgets - Показать все установленные бюджеты\n"
                            "/show - Показать все добавленные траты\n"
                            "/remove_expense <id> - Удалить трату по ID\n"
                            "/analysis <start_date> <start_time> <end_date> <end_time>. Формат даты и времени: YYYY-MM-DD HH:MM:SS\n"
                            "/help - Показать это сообщение\n")
    
    await update.message.reply_text(welcome_message)


async def show_help(update: Update, context: CallbackContext) -> None:
    help_text = (
        "Доступные команды:\n"
        "/start - Зарегистрироваться\n"
        "/add <сумма> <описание> - Добавить трату\n"
        "/set_budget <категория> <сумма> - Установить бюджет для категории\n"
        "/delete_budget <категория> - Удалить установленный бюджет для категории\n"
        "/show_budgets - Показать все установленные бюджеты\n"
        "/show - Показать все добавленные траты\n"
        "/remove_expense <id> - Удалить трату по ID\n"
        "/analysis <start_date> <start_time> <end_date> <end_time>. Формат даты и времени: YYYY-MM-DD HH:MM:SS\n"
        "/help - Показать это сообщение\n"
    )
    await update.message.reply_text(help_text)