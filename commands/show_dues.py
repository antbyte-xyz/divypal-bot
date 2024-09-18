from collections import defaultdict

from telegram import Update
from telegram.ext import ContextTypes
from utils.data import load_expenses


async def show_dues(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
        dues_summary.append(f"😎 {member}: {'gets' if due < 0 else 'owes'} ৳{abs(due):.2f}")

    if dues_summary:
        await update.message.reply_text("\n".join(dues_summary))
    else:
        await update.message.reply_text("No dues")