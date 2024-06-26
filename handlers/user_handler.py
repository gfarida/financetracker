"""
This module handles the registration and help functions for a Telegram bot. It provides
functionalities to register new users, display help messages with command details, and guide users
through using the bot.

Functions:
    start: Registers a new user or notifies them if they are already registered.
    show_help: Displays help information detailing available bot commands.
"""
from telegram import Update
from telegram.ext import CallbackContext

from models.finance_model import User, session


HELP_TEXT = (
    "Available commands:\n"
    "/start - Register\n"
    "/add <amount> <description> - Add an expense\n"
    "/set_budget <category> <amount> - Set a budget for a category\n"
    "/delete_budget <category> - Delete the set budget for a category\n"
    "/show_budgets - Show all set budgets\n"
    "/show - Show all added expenses\n"
    "/remove_expense <id> - Delete an expense by ID\n"
    "/analysis <start_date> <start_time> <end_date> <end_time>. "
    "Date and time format: YYYY-MM-DD HH:MM:SS\n"
    "/help - Show this message\n"
)


async def start(update: Update, context: CallbackContext) -> None:
    """
    Registers a new user in the system if they are not already registered, or welcomes them back if
    they are.

    This function checks if the user exists in the database. If the user does not exist, it
    registers them and sends a welcome message with a list of available commands. If the user is
    already registered, it sends a welcome back message instead.

    Args:
        update (Update): The update received from Telegram, which contains the user's message and
                         chat details.
        context (CallbackContext): The context object provided by the Telegram bot framework which
                                   carries data and settings related to the command being processed.

    Usage:
        User types: /start
    """
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    existing_user = session.query(User).filter(User.uid == user_id).first()

    if not existing_user:
        new_user = User(uid=user_id, name=user_name)
        session.add(new_user)
        session.commit()
        welcome_message = (
            "Hello! I am a finance management bot. You have successfully registered.\n"
        )
    else:
        welcome_message = "Hello! You are already registered.\n"

    welcome_message += HELP_TEXT
    await update.message.reply_text(welcome_message)


async def show_help(update: Update, context: CallbackContext) -> None:
    """
    Sends a help message to the user detailing all available commands and their usage.

    This function provides a list of all commands that the user can use with the bot,
    explaining how to use each command with examples.

    Args:
        update (Update): The update received from Telegram, containing the user's message and chat
                         details.
        context (CallbackContext): The context object provided by the Telegram bot framework.

    Usage:
        User types: /help
    """
    await update.message.reply_text(HELP_TEXT)
