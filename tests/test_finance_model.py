import unittest
from financetracker_bot.models.finance_model import User, Expense, Budget, session
import datetime

class TestFinanceModel(unittest.TestCase):

    def setUp(self):
        self.user = User(uid=1, name="Test User")
        session.add(self.user)
        session.commit()

    def tearDown(self):
        session.query(User).delete()
        session.query(Expense).delete()
        session.query(Budget).delete()
        session.commit()

    def test_user_creation(self):
        user = session.query(User).filter_by(uid=1).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Test User")

    def test_expense_creation(self):
        cur_date = datetime.datetime.now()
        expense = Expense(uid=self.user.uid, name="Lunch", category="Dining", amount=10.0, date=cur_date)
        session.add(expense)
        session.commit()

        stored_expense = session.query(Expense).filter_by(uid=self.user.uid).first()
        self.assertIsNotNone(stored_expense)
        self.assertEqual(stored_expense.name, "Lunch")
        self.assertEqual(stored_expense.category, "Dining")
        self.assertEqual(stored_expense.amount, 10.0)
        self.assertEqual(stored_expense.date, cur_date)

    def test_budget_creation(self):
        budget = Budget(uid=self.user.uid, category="Dining", amount=200.0)
        session.add(budget)
        session.commit()

        stored_budget = session.query(Budget).filter_by(uid=self.user.uid).first()
        self.assertIsNotNone(stored_budget)
        self.assertEqual(stored_budget.category, "Dining")
        self.assertEqual(stored_budget.amount, 200.0)

if __name__ == '__main__':
    unittest.main()
