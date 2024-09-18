from collections import defaultdict


def calculate_dues(expenses):
    total_due = defaultdict(int)

    for member, expense_details in expenses.items():
        for exp in expense_details:
            per_head = exp.price / len(exp.members)
            for selected_members in exp.members:
                total_due[selected_members] += per_head
            total_due[f"@{member}"] -= exp.price
    
    return total_due