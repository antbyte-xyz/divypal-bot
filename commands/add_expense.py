from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from data import load_expenses, load_members, save_expenses, save_members
from models.Expense import Expense


async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    members = load_members()
    expenses = load_expenses()
    username = update.effective_user.username
    print(username, members)

    if f'@{username}' not in members:
        await update.message.reply_text("You are not a member. Please ask someone else to add you to the members list before adding expenses.")
        return

    if not update.message.text.strip():
        await update.message.reply_text("Please provide expenses in the format:\n/item1 price1\nitem2 price2\n...")
        return

    lines = update.message.text.splitlines()[1:]
    total_amount = 0
    expense_details = []

    for line in lines:
        try:
            item, price = line.rsplit(' ', 1)
            price = float(price)
            total_amount += price
            expense_details.append(Expense(item, price, datetime.now(), members.copy()))
        except ValueError:
            await update.message.reply_text(f"Invalid format for '{line}'. Please use 'item price'.")
            return

    if not members:
        await update.message.reply_text("No members available to split the expenses. Please add members first.")
        return

    if username not in expenses:
        expenses[username] = []
    expenses[username].extend(expense_details)

    save_members(members=members)
    save_expenses(expenses=expenses)
    await update.message.reply_text(
        "Expenses recorded:\n" + "\n".join(str(exp) for exp in expense_details) +
        f"\nTotal amount: ৳{total_amount}\n"
    )