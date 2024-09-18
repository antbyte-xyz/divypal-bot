from telegram import Update
from telegram.ext import ContextTypes

from data import load_members, save_members


async def members_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    members = load_members()
    if not context.args:
        if members:
            await update.message.reply_text(f"Current members: {', '.join(members)}\nTotal members: {len(members)}")
        else:
            await update.message.reply_text("No members added yet. Use /members add <name> to add members.")

    elif context.args[0].lower() == "add":
        new_members = context.args[1:]
        for member in new_members:
            if member not in members:
                members.append(member)
        save_members(members=members)
        await update.message.reply_text(f"Updated member list: {', '.join(members)}")

    elif context.args[0].lower() == "remove":
        to_remove = context.args[1:]
        members[:] = [m for m in members if m not in to_remove]
        save_members(members=members)
        await update.message.reply_text(f"Updated member list: {', '.join(members)}")
    else:
        await update.message.reply_text("Invalid command. Use /members, /members add <name>, /members remove <name>")
