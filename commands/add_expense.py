from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from data import expenses, members
from models.Expense import Expense


async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /add_expense command"""
    username = update.effective_user.username
    print(username, members)

    # Guard statement: Check if the user is in the members list
    if f'@{username}' not in members:
        await update.message.reply_text("You are not a member. Please ask someone else to add you to the members list before adding expenses.")
        return

    if not update.message.text.strip():
        await update.message.reply_text("Please provide expenses in the format:\n/item1 price1\nitem2 price2\n...")
        return

    # Split the message into lines
    lines = update.message.text.splitlines()[1:]  # Skip the first line (the command itself)
    total_amount = 0
    expense_details = []

    # Process each line of input
    for line in lines:
        try:
            item, price = line.rsplit(' ', 1)  # Split on the last space
            price = float(price)  # Convert price to float
            total_amount += price
            expense_details.append(Expense(item, price, datetime.now(), members.copy()))  # Add current date
        except ValueError:
            await update.message.reply_text(f"Invalid format for '{line}'. Please use 'item price'.")
            return

    if not members:
        await update.message.reply_text("No members available to split the expenses. Please add members first.")
        return

    # Calculate the split amount
    split_amount = total_amount / len(members)

    # Store the expenses in the dictionary
    if username not in expenses:
        expenses[username] = []
    expenses[username].extend(expense_details)

    await update.message.reply_text(
        f"Expenses recorded:\n" + "\n".join(str(exp) for exp in expense_details) +
        f"\nTotal amount: {total_amount}\nEach member owes:{split_amount:.2f}"
    )