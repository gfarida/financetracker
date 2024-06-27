.. Finance Tracker documentation master file, created by
   sphinx-quickstart on Wed Jun 19 21:17:27 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Finance Tracker's documentation!
===========================================

**Overview**

This Telegram bot empowers users to manage their finances more effectively. It integrates key features for tracking expenses, analyzing spending patterns, and adhering to budgets, thereby simplifying personal finance management directly through Telegram.

**Key Features**

- **Expense Tracking**
  - Allows users to log expenses by entering details such as the expense name/category and the amount. Each entry is automatically timestamped with the date and time of submission.
  
- **Automatic Category Classification**
  - Users have the option to enter expenses without categorizing them; the bot utilizes OpenAI technology to intelligently classify these expenses based on their descriptions.
  
- **Financial Reporting**
  - On request, the bot generates detailed financial reports covering specified time frames (e.g., monthly or yearly). These reports include visual charts that break down spending by category, total expenditures, and other relevant financial analytics.
  
- **Budget Management**
  - Users can set financial limits for various spending categories. The bot monitors these expenditures and updates users on their progress, helping them stay within their budgetary constraints.

This bot is designed to offer a seamless and intuitive experience for personal finance management, leveraging advanced AI to automate and personalize financial tracking and analysis.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   handlers
   main
   modules
   utils

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

