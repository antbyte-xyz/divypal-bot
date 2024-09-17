from telegram import Update
from telegram.ext import ContextTypes

from data import expenses


async def settle_up(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /settleup command to clear all expenses."""
    global expenses
    expenses.clear()  # Clear all recorded expenses
    await update.message.reply_text("All expenses have been cleared. You can start fresh!")