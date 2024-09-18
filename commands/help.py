from telegram import Update
from telegram.ext import ContextTypes


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"👋 Hi {user.mention_html()}! I'm your expense tracking bot. \n"
        "\n"
        "/members to view and edit the list of members\n"
        "    <code>/members add &lt;name&gt;</code> to add a member\n"
        "    <code>/members remove &lt;name&gt;</code> to remove a member\n"
        "    <code>/members</code> to show all members\n"
        "\n"
        "/addx to add expenses.\n"
        "    The items should be list in this format:\n"
        "    <code>/addx</code>\n"
        "    <code>3kg fish 300</code>\n"
        "    <code>potato and tomato 100</code>\n"
        "\n"
        "/showx to show expenses\n"
        "\n"
        "/status to show status for each member\n"
        "\n"
        "/settleup to settle up\n"
        "    <b>CAUTION</b>: All you expenses will be deleted"
        "\n"
        "/report to generate a report of all expenses"
    )