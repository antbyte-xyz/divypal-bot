import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from commands.add_expense import add_expense
from commands.help import help
from commands.members_command import members_command
from commands.settle_up import settle_up, settle_up_callback
from commands.show_dues import show_dues
from commands.show_expenses import show_expenses

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("members", members_command))
    application.add_handler(CommandHandler("addx", add_expense))
    application.add_handler(CommandHandler("showx", show_expenses))
    application.add_handler(CommandHandler("status", show_dues))
    application.add_handler(CommandHandler("settleup", settle_up))
    application.add_handler(CallbackQueryHandler(settle_up_callback, pattern='^(confirm|cancel)_settleup$'))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
