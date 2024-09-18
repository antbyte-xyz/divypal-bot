from collections import defaultdict


def calculate_dues(expenses):
    total_due = defaultdict(int)
    dues_summary = []
    for member, expense_details in expenses.items():
        for exp in expense_details:
            per_head = exp.price / len(exp.members)
            for selected_members in exp.members:
                total_due[selected_members] += per_head
            total_due[f"@{member}"] -= exp.price
    
    for member, due in total_due.items():
        dues_summary.append(
            f"😎 {member} {'gets' if due < 0 else 'owes'} ৳{abs(due):.2f}")

    return dues_summary