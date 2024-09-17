from telegram import Update
from telegram.ext import ContextTypes


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"👋 Hi {user.mention_html()}! I'm your expense tracking bot. \n"
        "/members to view and edit the list of members\n"
        "/addx to add expenses.\n"
        "/showx to show expenses\n"
        "/dues to show dues for each member\n"
        "/settleup to settle up"
    )