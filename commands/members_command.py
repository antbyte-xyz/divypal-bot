from telegram import Update
from telegram.ext import ContextTypes

from data import *


async def members_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    members = load_members()
    """Handle the /members command"""
    if not context.args:
        # If no arguments, display current members
        if members:
            await update.message.reply_text(f"Current members: {', '.join(members)}")
        else:
            await update.message.reply_text("No members added yet. Use /members add <name> to add members.")
    elif context.args[0].lower() == "add":
        # Add new member(s)
        new_members = context.args[1:]
        for member in new_members:
            if member not in members:
                members.append(member)
        save_members(members=members)
        await update.message.reply_text(f"Updated member list: {', '.join(members)}")
    elif context.args[0].lower() == "remove":
        # Remove member(s)
        to_remove = context.args[1:]
        members[:] = [m for m in members if m not in to_remove]
        save_members(members=members)
        await update.message.reply_text(f"Updated member list: {', '.join(members)}")
    else:
        await update.message.reply_text("Invalid command. Use /members, /members add <name>, /members remove <name>")