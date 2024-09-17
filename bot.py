import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler

from commands.add_expense import add_expense
from commands.help import help
from commands.members_command import members_command
from commands.settle_up import settle_up
from commands.show_dues import show_dues
from commands.show_expenses import show_expenses

# Load environment variables from .env file
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("members", members_command))
    application.add_handler(CommandHandler("addx", add_expense))
    application.add_handler(CommandHandler("showx", show_expenses))
    application.add_handler(CommandHandler("status", show_dues))
    application.add_handler(CommandHandler("settleup", settle_up))  # Add settle up command handler

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
