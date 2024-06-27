"""
This module provides functionality to classify expenses into predefined categories
using OpenAI's GPT-3.5-turbo-instruct model. It utilizes the OpenAI API to analyze
the description of an expense and determine the appropriate category.
"""

from config.config import OPENAI_API_KEY
from openai import OpenAI as OriginalOpenAI

class OpenAI:
    """
    A wrapper class for the OpenAI API client to classify expense descriptions
    into predefined categories.
    """

    def __init__(self, api_key=None):
        """
        Initialize the OpenAI client with the provided API key or the default key from config.

        Args:
            api_key (str, optional): The API key to use. If not provided, the default key from
                                     the configuration will be used.
        """
        self.api_key = api_key or OPENAI_API_KEY
        self.client = OriginalOpenAI(api_key=self.api_key)

    def classify_expense(self, description):
        """
        Classify an expense description into one of the predefined categories.

        Args:
            description (str): The description of the expense to classify.

        Returns:
            str: The name of the category that the expense belongs to. If the category
                 cannot be determined, 'Other' is returned.
        """
        expense_categories = [
            "Groceries",
            "Rent",
            "Utilities",
            "Transportation",
            "Dining",
            "Entertainment",
            "Health",
            "Education",
            "Clothing",
            "Other",
        ]

        prompt = (
            f"Which of the following categories does the expense '{description}' belong to? "
            f"{', '.join(expense_categories)}. "
            "User may answer in any language. Answer with one word - the name of the category "
            "in English. If you don't know answer Other."
        )

        response = self.client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=5,
        )

        resp = response.choices[0].text.strip()

        if resp not in expense_categories:
            resp = "Other"

        return resp
