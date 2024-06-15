import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

from config.config import TELEGRAM_BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я бот для управления финансами.')

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.run_polling()

if __name__ == '__main__':
    main()
