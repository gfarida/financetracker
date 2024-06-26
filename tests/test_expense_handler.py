import unittest
from unittest.mock import AsyncMock, patch
from telegram import Update, User as TelegramUser, Message, Chat
from telegram.ext import CallbackContext
from models.finance_model import Expense, User, Budget, session
from handlers.expense_handler import add_expense, show_expenses, delete_expense
import datetime

class TestExpenseHandler(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.user = User(uid=123, name="Test User")
        session.add(self.user)
        session.commit()

    def tearDown(self):
        session.query(Expense).delete()
        session.query(User).delete()
        session.query(Budget).delete()
        session.commit()
        session.rollback()

    def create_update(self, text):
        return Update(
            update_id=1,
            message=Message(
                message_id=1,
                date=datetime.datetime.now(),
                chat=Chat(id=123, type="private"),
                from_user=TelegramUser(id=123, first_name="Test", is_bot=False),
                text=text,
            ),
        )

    @patch('telegram.Message.reply_text', new_callable=AsyncMock)
    async def test_add_expense(self, mock_reply_text):
        update = self.create_update("/add 100 Lunch")
        context = CallbackContext.from_update(update, application=None)
        context.args = ["100", "Lunch"]

        await add_expense(update, context)

        expense = session.query(Expense).filter_by(uid=123).first()
        self.assertIsNotNone(expense)
        self.assertEqual(expense.amount, 100.0)
        self.assertIsNotNone(["Groceries", "Rent", "Utilities", "Transportation", "Dining", "Entertainment", "Health", "Education", "Clothing", "Other"])

        mock_reply_text.assert_called()

    @patch('telegram.Message.reply_text', new_callable=AsyncMock)
    async def test_show_expenses(self, mock_reply_text):
        cur_date = datetime.datetime.now()
        expense1 = Expense(uid=123, category="Dining", amount=10, date=cur_date)
        expense2 = Expense(uid=123, category="Dining", amount=5, date=cur_date)
        session.add(expense1)
        session.add(expense2)
        session.commit()

        update = self.create_update("/show_expenses")
        context = CallbackContext.from_update(update, application=None)

        await show_expenses(update, context)

        expected_message = (
            f"Дата: *{expense1.date.strftime('%Y-%m-%d %H:%M:%S')}*, трата: *{expense1.amount}*, категория: *{expense1.category}*, ID: *{expense1.eid}*\n"
            f"Дата: *{expense2.date.strftime('%Y-%m-%d %H:%M:%S')}*, трата: *{expense2.amount}*, категория: *{expense2.category}*, ID: *{expense2.eid}*"
        )
        mock_reply_text.assert_called_with(f'Ваши траты:\n{expected_message}', parse_mode='Markdown')

    @patch('telegram.Message.reply_text', new_callable=AsyncMock)
    async def test_delete_expense(self, mock_reply_text):
        cur_date = datetime.datetime.now()
        expense = Expense(uid=123, category="Dining", amount=10, date=cur_date)
        session.add(expense)
        session.commit()

        update = self.create_update("/delete 1")
        context = CallbackContext.from_update(update, application=None)
        context.args = ["1"]

        await delete_expense(update, context)

        deleted_expense = session.query(Expense).filter_by(eid=1).first()
        self.assertIsNone(deleted_expense)
        mock_reply_text.assert_called_with("Трата с ID 1 успешно удалена!")


if __name__ == 'main':
    unittest.main()