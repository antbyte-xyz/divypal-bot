---
title: Divypal
emoji: 💸
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
---
# Divypal

This Telegram bot helps users track shared expenses within a group. It allows members to add expenses, view balances, and manage group members.

## Features

- Add expenses with item name, price, and involved members
- View current balances for all group members
- Add or remove members from the expense tracking group
- Secure storage of expense data in JSON format
- Settle up balances with other members
- Get detailed information about expenses and balances

## Requirements

- Python 3.11+
- Required packages are listed in the `requirements.txt` file

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```
3. Run the bot:

```bash
python bot.py
```
## Usage

Start a chat with the bot on Telegram and use the following commands:

- `/help` - Show details about all commands
- `/members` - Show all members in the expense tracking group
- `/members add @username` - Add a new member to the expense tracking group
- `/members remove @username` - Remove a member from the expense tracking group
- `/addx <item> <price>` - Add a new expense
- `/showx` - View current balances for all members
- `/settleup @username` - Settle up balances with other members
- `/report` - Generate a PDF file with all the expenses and status of each members.