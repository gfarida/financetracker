import unittest
from unittest.mock import patch, MagicMock
from utils.openai_util import classify_expense

class TestClassifyExpense(unittest.TestCase):

    @patch('utils.openai_util.OpenAI')
    def test_classify_expense_groceries(self, MockOpenAI):
        mock_completions = MagicMock()
        mock_completions.choices = [{'text': 'Groceries'}]
        MockOpenAI.return_value.completions.return_value = mock_completions

        description = "Bought groceries at the store"
        result = classify_expense(description)
        self.assertEqual(result, "Groceries")

    @patch('utils.openai_util.OpenAI')
    def test_classify_expense_other(self, MockOpenAI):
        mock_completions = MagicMock()
        mock_completions.choices = [{'text': 'Other'}]
        MockOpenAI.return_value.completions.return_value = mock_completions

        description = "Paid for parking"
        result = classify_expense(description)
        self.assertEqual(result, "Other")

if __name__ == '__main__':
    unittest.main()
