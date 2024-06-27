"""
This module sets up and runs a Telegram bot for financial management commands using
the `python-telegram-bot` library. It handles starting the bot, adding and showing expenses,
setting and deleting budgets, and providing financial analysis.

Handlers for these commands are imported from separate modules.
"""
import logging
from telegram.ext import Application, CommandHandler
from financetracker_bot.handlers.user_handler import start, show_help
from financetracker_bot.handlers.expense_handler import add_expense, show_expenses, delete_expense
from financetracker_bot.handlers.budget_handler import set_budget, delete_budget, show_budgets, financial_analysis

from config.config import TELEGRAM_BOT_TOKEN


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def main():
    """
    Sets up the Telegram bot application with command handlers and starts polling for updates.

    Command Handlers:
        /start: Starts the bot and shows a welcome message.
        /add: Adds an expense.
        /show: Shows a list of expenses.
        /set_budget: Sets a budget.
        /delete: Deletes an expense.
        /delete_budget: Deletes a budget.
        /show_budgets: Shows a list of budgets.
        /analysis: Provides financial analysis.
        /help: Shows the help message with command descriptions.
    """
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_expense))
    application.add_handler(CommandHandler("show", show_expenses))
    application.add_handler(CommandHandler("set_budget", set_budget))
    application.add_handler(CommandHandler("delete", delete_expense))
    application.add_handler(CommandHandler("delete_budget", delete_budget))
    application.add_handler(CommandHandler("show_budgets", show_budgets))
    application.add_handler(CommandHandler("analysis", financial_analysis))
    application.add_handler(CommandHandler("help", show_help))
    application.run_polling()


if __name__ == '__main__':
    main()
