"""
This module provides functionality to classify expenses into predefined categories
using OpenAI's GPT-3.5-turbo-instruct model. It utilizes the OpenAI API to analyze
the description of an expense and determine the appropriate category.
"""

from openai import OpenAI
from config.config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


def classify_expense(description):
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

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=5,
    )

    resp = response.choices[0].text.strip()

    if resp not in expense_categories:
        resp = "Other"

    return resp
