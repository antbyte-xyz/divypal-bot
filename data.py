import json
import os
from datetime import datetime

from models.Expense import Expense

# File paths for persistence
MEMBERS_FILE = 'members.json'
EXPENSES_FILE = 'expenses.json'

def save_members(members: list[str]):
    with open(MEMBERS_FILE, 'w') as f:
        json.dump(members, f)

def load_members() -> list[str]:
    if os.path.exists(MEMBERS_FILE):
        with open(MEMBERS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_expenses(expenses: dict[str, list[Expense]]) -> None:
    expenses_data = {
        username: [
            {
                **expense.__dict__,
                'date': expense.date.isoformat()  # Convert datetime to string
            } for expense in expense_list
        ] for username, expense_list in expenses.items()
    }
    with open(EXPENSES_FILE, 'w') as f:
        json.dump(expenses_data, f)

def load_expenses() -> dict[str, list[Expense]]:
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'r') as f:
            expenses_data = json.load(f)
            return {
                username: [
                    Expense(
                        item=data['item'],
                        price=data['price'],
                        date=datetime.fromisoformat(data['date']),  # Convert string back to datetime
                        members=data['members']
                    ) for data in expense_list
                ] for username, expense_list in expenses_data.items()
            }
    return {}