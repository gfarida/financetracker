import unittest
from unittest.mock import AsyncMock, patch
from telegram import Update, User as TelegramUser, Message, Chat
from telegram.ext import CallbackContext
from models.finance_model import Budget, Expense, User, session
from handlers.budget_handler import set_budget, delete_budget, show_budgets
from handlers.expense_handler import add_expense
import datetime
import logging

logging.getLogger('asyncio').setLevel(logging.CRITICAL)

class TestBudgetHandler(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.user = User(uid=123, name="Test User")
        session.add(self.user)
        session.commit()

    def tearDown(self):
        session.query(Budget).delete()
        session.query(Expense).delete()
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
                from_user=TelegramUser(id=123, first_name="Test", is_bot=False),
                text=text,
            ),
        )

    @patch('telegram.Message.reply_text', new_callable=AsyncMock)
    async def test_set_budget(self, mock_reply_text):
        update = self.create_update("/set_budget Dining 500")
        context = CallbackContext.from_update(update, application=None)
        context.args = ["Dining", "500"]

        await set_budget(update, context)

        budget = session.query(Budget).filter_by(uid=123, category="Dining").first()
        self.assertIsNotNone(budget)
        self.assertEqual(budget.amount, 500.0)

        mock_reply_text.assert_called_with('Установлен бюджет: 500.0 для категории Dining')

    @patch('telegram.Message.reply_text', new_callable=AsyncMock)
    async def test_delete_budget(self, mock_reply_text):
        budget = Budget(uid=123, category="Dining", amount=500)
        session.add(budget)
        session.commit()

        update = self.create_update("/delete_budget Dining")
        context = CallbackContext.from_update(update, application=None)
        context.args = ["Dining"]

        await delete_budget(update, context)

        budget = session.query(Budget).filter_by(uid=123, category="Dining").first()
        self.assertIsNone(budget)

        mock_reply_text.assert_called_with('Бюджет для категории Dining удален! Бюджет установлен в бесконечность.')

    @patch('telegram.Message.reply_text', new_callable=AsyncMock)
    @patch('handlers.expense_handler.add_expense', new_callable=AsyncMock)
    async def test_show_budgets(self, mock_add_expense, mock_reply_text):
        budget = Budget(uid=123, category="Dining", amount=500)
        session.add(budget)
        session.commit()

        update_add = self.create_update("/add 100 Lunch")
        context_add = CallbackContext.from_update(update_add, application=None)
        context_add.args = ["100", "Lunch"]

        await add_expense(update_add, context_add)

        update_show = self.create_update("/show_budgets")
        context_show = CallbackContext.from_update(update_show, application=None)

        await show_budgets(update_show, context_show)

        expected_message = (
            f"Категория: *Dining* - Бюджет: *500.0.* Израсходовано: *20.00% * (100.0 / 500.0)\n"
        )
        mock_reply_text.assert_called_with(f'Ваши установленные бюджеты:\n{expected_message}', parse_mode='Markdown')

if __name__ == 'main':
    unittest.main()