from collections import defaultdict

from telegram import Update
from telegram.ext import ContextTypes
from data import *


async def show_dues(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /dues command"""
    expenses = load_expenses()
    dues_summary = []
    total_due = defaultdict(int)

    for member, expense_details in expenses.items():
        for exp in expense_details:
            per_head = exp.price / len(exp.members)
            for selected_members in exp.members:
                total_due[selected_members] += per_head
            total_due[f"@{member}"] -= exp.price


    for member, due in total_due.items():
        dues_summary.append(f"{member}: {'gets' if due < 0 else 'owes'} {abs(due):.2f}")

    await update.message.reply_text("\n".join(dues_summary))