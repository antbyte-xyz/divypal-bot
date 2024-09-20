from pytz import timezone
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from utils.data import load_expenses
from utils.pdf_generator import generate_expense_report


async def generate_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate and send a PDF report of all expenses."""
    expenses = load_expenses()
    if not expenses:
        await update.message.reply_text("No expenses recorded yet.")
        return

    pdf_buffer = generate_expense_report(expenses)

    await update.message.reply_document(
        document=pdf_buffer,
        filename=f"expense_report_{datetime.now(timezone('Asia/Dhaka')).strftime('%d %b, %Y')}.pdf",
        caption="Here's the expense report."
    )
