from collections import defaultdict

from telegram import Update
from telegram.ext import ContextTypes

from data import expenses


async def show_expenses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /show_expenses command"""
    if not expenses:
        await update.message.reply_text("No expenses recorded yet.")
        return

    expense_summary = []
    for member, details in expenses.items():
        # Group expenses by date
        expenses_by_date = defaultdict(list)
        for exp in details:
            expenses_by_date[exp.date.strftime('%d %b, %Y')].append(exp)

        total_member_expenses = 0
        member_summary = [f"😎 @{member}:"]
        for date, exps in expenses_by_date.items():
            member_summary.append(f"🗓 {date}")  # Add calendar emoji before the date
            for exp in exps:
                member_summary.append(str(exp))  # Convert Expense instance to string
                total_member_expenses += exp.price
            member_summary.append("")  # Add a blank line after each date

        member_summary.append(f"Total: {total_member_expenses:.2f}")
        expense_summary.append("\n".join(member_summary))

    await update.message.reply_text("Recorded Expenses:\n" + "\n\n".join(expense_summary))