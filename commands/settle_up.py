from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.data import load_expenses, save_expenses

async def settle_up(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /settleup command to clear all expenses."""
    keyboard = [
        [
            InlineKeyboardButton("Yes, settle up", callback_data='confirm_settleup'),
            InlineKeyboardButton("No, cancel", callback_data='cancel_settleup'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Are you sure you want to settle up? This will clear all expenses.",
        reply_markup=reply_markup
    )

async def settle_up_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the callback from the settle up confirmation."""
    query = update.callback_query
    await query.answer()

    if query.data == 'confirm_settleup':
        expenses = load_expenses()
        expenses.clear()
        save_expenses(expenses=expenses)
        await query.edit_message_text("All expenses have been cleared. You can start fresh!")
    else:
        await query.edit_message_text("Settle up cancelled.")
