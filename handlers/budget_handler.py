from telegram import Update
from telegram.ext import CallbackContext
from models.finance_model import Budget, session, User, Expense
import datetime
import matplotlib.pyplot as plt

async def set_budget(update: Update, context: CallbackContext) -> None:
    try:
        args = context.args
        category = args[0]
        amount = float(args[1])
        user_id = update.effective_user.id  # Получаем ID пользователя
        user = session.query(User).filter(User.uid == user_id).first()

        if not user:
            await update.message.reply_text('Сначала зарегистрируйтесь с помощью команды /start.')
            return

        budget = session.query(Budget).filter_by(uid=user.uid, category=category).first()
        if budget:
            budget.amount = amount
        else:
            budget = Budget(uid=user.uid, category=category, amount=amount)
            session.add(budget)
        
        session.commit()
        await update.message.reply_text(f'Установлен бюджет: {amount} для категории {category}')
    except (IndexError, ValueError):
        await update.message.reply_text('Использование: /set_budget <категория> <сумма>')

async def delete_budget(update: Update, context: CallbackContext) -> None:
    try:
        args = context.args
        if len(args) < 1:
            await update.message.reply_text('Использование: /delete_budget <категория>')
            return

        category = args[0]
        user_id = update.effective_user.id

        budget = session.query(Budget).filter_by(uid=user_id, category=category).first()
        if budget:
            session.delete(budget)
            session.commit()
            await update.message.reply_text(f'Бюджет для категории {category} удален! Бюджет установлен в бесконечность.')
        else:
            await update.message.reply_text(f'Бюджет для категории {category} не найден.')
    except Exception as e:
        print(e)
        await update.message.reply_text('Произошла ошибка при удалении бюджета.')


async def show_budgets(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.effective_user.id

        user = session.query(User).filter(User.uid == user_id).first()
        if not user:
            await update.message.reply_text('Сначала зарегистрируйтесь с помощью команды /start.')
            return

        budgets = session.query(Budget).filter_by(uid=user_id).all()
        if not budgets:
            await update.message.reply_text('У вас нет установленных бюджетов.')
            return

        response = "Ваши установленные бюджеты:\n"
        for budget in budgets:
            response += f"Категория: *{budget.category}* - Бюджет: *{budget.amount}*\n"

        await update.message.reply_text(response, parse_mode='Markdown')
    except Exception as e:
        print(e)
        await update.message.reply_text('Произошла ошибка при получении бюджетов.')



async def financial_analysis(update: Update, context: CallbackContext) -> None:
    try:
        args = context.args
        start_date_str = args[0]
        start_time_str = args[1]
        end_date_str = args[2]
        end_time_str = args[3]
        
        start_datetime = datetime.datetime.strptime(start_date_str + ' ' + start_time_str, '%Y-%m-%d %H:%M:%S')
        end_datetime = datetime.datetime.strptime(end_date_str + ' ' + end_time_str, '%Y-%m-%d %H:%M:%S')

        user_id = update.effective_user.id

        expenses = session.query(Expense).filter(
            Expense.uid == user_id,
            Expense.date >= start_datetime,
            Expense.date <= end_datetime
        ).all()

        total_expenses = sum(expense.amount for expense in expenses)

        categories = set(expense.category for expense in expenses)
        category_expenses = {
            category: sum(expense.amount for expense in expenses if expense.category == category)
            for category in categories
        }

        response = f"Финансовый анализ с {start_date_str} {start_time_str} по {end_date_str} {end_time_str}:\n"
        response += f"Общие расходы: {total_expenses}\n\n"
        response += "Расходы по категориям:\n"
        for category, amount in category_expenses.items():
            response += f"{category}: {amount}\n"

        labels = list(category_expenses.keys())
        sizes = list(category_expenses.values())
        colors = plt.cm.viridis_r([float(i) / len(labels) for i in range(len(labels))])  # Генерация цветов по количеству категорий

        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, wedgeprops={'edgecolor': 'black'})
        ax.legend(wedges, labels, title="Категории", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        ax.set_title('Расходы по категориям')

        pie_chart_path = 'pie_chart.png'
        plt.savefig(pie_chart_path)

        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(pie_chart_path, 'rb'), caption=response)

    except IndexError:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Пожалуйста, используйте формат: /financial_analysis <start_date> <start_time> <end_date> <end_time>. Пример формата даты и времени: YYYY-MM-DD HH:MM:SS')
    except Exception as e:
        print(e)
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Произошла ошибка при выполнении анализа.')
