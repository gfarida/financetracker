import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from handlers.user_handler import start
from handlers.expense_handler import add_expense, show_expenses, delete_expense
from handlers.budget_handler import set_budget, delete_budget

from config.config import TELEGRAM_BOT_TOKEN


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_expense))
    application.add_handler(CommandHandler("show", show_expenses))
    application.add_handler(CommandHandler("set_budget", set_budget))
    application.add_handler(CommandHandler("delete", delete_expense))
    application.add_handler(CommandHandler("delete_budget", delete_budget))

    application.run_polling()


if __name__ == '__main__':
    main()
