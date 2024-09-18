from telegram import Update
from telegram.ext import ContextTypes
from utils.data import load_expenses
from utils.calculate_dues import calculate_dues


async def show_dues(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    expenses = load_expenses()
    dues_summary = calculate_dues(expenses)
    if dues_summary:
        await update.message.reply_text("\n".join(dues_summary))
    else:
        await update.message.reply_text("No dues")
