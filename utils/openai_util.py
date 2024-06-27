"""
This module provides functionality to classify expenses into predefined categories
using OpenAI's GPT-3.5-turbo-instruct model. It utilizes the OpenAI API to analyze
the description of an expense and determine the appropriate category.
"""

from openai import OpenAI
from config.config import OPENAI_API_KEY

from utils.translation import _


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
        _("Groceries"),
        _("Rent"),
        _("Utilities"),
        _("Transportation"),
        _("Dining"),
        _("Entertainment"),
        _("Health"),
        _("Education"),
        _("Clothing"),
        _("Other"),
    ]

    prompt = _(
        "Which of the following categories does the expense '{}' belong to? "
        "{}. "
        "User may answer in any language. Answer with one word - the name of the category "
        "in English. If you don't know answer Other."
    ).format(description, ', '.join(expense_categories))

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=5,
    )

    resp = response.choices[0].text.strip()

    if resp not in expense_categories:
        resp = _("Other")

    return resp
