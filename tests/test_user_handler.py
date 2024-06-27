import unittest
from unittest.mock import AsyncMock, patch
from telegram import Update, User as TelegramUser, Message, Chat
from telegram.ext import CallbackContext
from models.finance_model import User, session
from handlers.user_handler import start, show_help
import datetime

class TestUserHandler(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        session.query(User).delete()
        session.commit()
        session.rollback()

    def tearDown(self):
        session.query(User).delete()
        session.commit()
        session.rollback()

    def create_update(self, text):
        return Update(
            update_id=1,
            message=Message(
                message_id=1,
                date=datetime.datetime.now(),
                chat=Chat(id=123, type="private"),
                from_user=TelegramUser(id=123, first_name="TestUser", is_bot=False),
                text=text,
            ),
        )

    @patch('telegram.Message.reply_text', new_callable=AsyncMock)
    async def test_start_new_user(self, mock_reply_text):
        update = self.create_update("/start")
        context = CallbackContext.from_update(update, application=None)

        await start(update, context)

        user = session.query(User).filter_by(uid=123).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "TestUser")

        welcome_message = (
            'Hello! I am a finance management bot. You have successfully registered.\n'
            'Available commands:\n'
            '/start - Register\n'
            '/add <amount> <description> - Add an expense\n'
            '/set_budget <category> <amount> - Set a budget for a category\n'
            '/delete_budget <category> - Delete the set budget for a category\n'
            '/show_budgets - Show all set budgets\n'
            '/show - Show all added expenses\n'
            '/delete <id> - Delete an expense by ID\n'
            '/analysis <start_date> <start_time> <end_date> <end_time>. '
            'Date and time format: YYYY-MM-DD HH:MM:SS\n'
            '/help - Show this message\n'
        )

        mock_reply_text.assert_called_with(welcome_message)

    @patch('telegram.Message.reply_text', new_callable=AsyncMock)
    async def test_start_existing_user(self, mock_reply_text):
        user = User(uid=123, name="TestUser")
        session.add(user)
        session.commit()

        update = self.create_update("/start")
        context = CallbackContext.from_update(update, application=None)

        await start(update, context)

        welcome_message = (
            'Hello! You are already registered.\n'
            'Available commands:\n'
            '/start - Register\n'
            '/add <amount> <description> - Add an expense\n'
            '/set_budget <category> <amount> - Set a budget for a category\n'
            '/delete_budget <category> - Delete the set budget for a category\n'
            '/show_budgets - Show all set budgets\n'
            '/show - Show all added expenses\n'
            '/delete <id> - Delete an expense by ID\n'
            '/analysis <start_date> <start_time> <end_date> <end_time>. '
            'Date and time format: YYYY-MM-DD HH:MM:SS\n'
            '/help - Show this message\n'
        )
        mock_reply_text.assert_called_with(welcome_message)

    @patch('telegram.Message.reply_text', new_callable=AsyncMock)
    async def test_show_help(self, mock_reply_text):
        update = self.create_update("/help")
        context = CallbackContext.from_update(update, application=None)

        await show_help(update, context)

        help_message = (
            "Available commands:\n"
            "/start - Register\n"
            "/add <amount> <description> - Add an expense\n"
            "/set_budget <category> <amount> - Set a budget for a category\n"
            "/delete_budget <category> - Delete the set budget for a category\n"
            "/show_budgets - Show all set budgets\n"
            "/show - Show all added expenses\n"
            "/delete <id> - Delete an expense by ID\n"
            "/analysis <start_date> <start_time> <end_date> <end_time>. "
            "Date and time format: YYYY-MM-DD HH:MM:SS\n"
            "/help - Show this message\n"
        )
        mock_reply_text.assert_called_with(help_message)

if __name__ == 'main':
    unittest.main()
