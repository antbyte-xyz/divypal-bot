from telegram import Update
from telegram.ext import ContextTypes
from data import *

async def settle_up(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /settleup command to clear all expenses."""
    expenses = load_expenses()
    expenses.clear()  # Clear all recorded expenses
    save_expenses(expenses=expenses)
    await update.message.reply_text("All expenses have been cleared. You can start fresh!")