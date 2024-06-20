import unittest
from unittest.mock import patch, MagicMock
from utils.openai_util import OpenAI

class TestClassifyExpense(unittest.TestCase):

    @patch('utils.openai_util.OriginalOpenAI')
    def test_classify_expense_groceries(self, MockOpenAI):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(text='Groceries')]
        MockOpenAI.return_value.completions.create.return_value = mock_response

        openai = OpenAI()
        description = "Pizza and sushi"
        result = openai.classify_expense(description)
        self.assertEqual(result, "Groceries")

    @patch('utils.openai_util.OriginalOpenAI')
    def test_classify_expense_other(self, MockOpenAI):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(text='Something')]
        MockOpenAI.return_value.completions.create.return_value = mock_response

        openai = OpenAI()
        description = "Paid for something in a store"
        result = openai.classify_expense(description)
        self.assertEqual(result, "Other")

if __name__ == 'main':
    unittest.main()