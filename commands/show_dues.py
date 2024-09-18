from telegram import Update
from telegram.ext import ContextTypes
from utils.data import load_expenses
from utils.calculate_dues import calculate_dues


async def show_dues(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    expenses = load_expenses()
    dues_summary = []
    total_due = calculate_dues(expenses)

    for member, due in total_due.items():
        dues_summary.append(
            f"😎 {member} {'gets' if due < 0 else 'owes'} ৳{abs(due):.2f}")

    if dues_summary:
        await update.message.reply_text("\n".join(dues_summary))
    else:
        await update.message.reply_text("No dues")
