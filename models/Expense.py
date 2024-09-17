class Expense:
    def __init__(self, item, price, date, members):
        self.item = item
        self.price = price
        self.date = date
        self.members = members

    def __str__(self):
        return f"{self.item}: ৳{self.price}"