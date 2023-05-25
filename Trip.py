class TripExpense:
    def __init__(self):
        self.users = ['A', 'B', 'C', 'D', 'E']
        self.expenses = []
        self.payments = []
        self.receipts = []

    def add_expense(self, user, amount, description):
        self.expenses.append({'user': user, 'amount': amount, 'description': description})

    def upload_receipt(self, receipt):
        self.receipts.append(receipt)

    def tag_members(self, expense_index, members):
        if expense_index < len(self.expenses):
            self.expenses[expense_index]['members'] = members

    def make_payment(self, from_user, to_user, amount):
        self.payments.append({'from': from_user, 'to': to_user, 'amount': amount})

    def close_trip(self):
        total_expenses = sum(expense['amount'] for expense in self.expenses)
        per_person_expense = total_expenses / len(self.users)

        for user in self.users:
            payments_to_user = sum(payment['amount'] for payment in self.payments if payment['to'] == user)
            payments_from_user = sum(payment['amount'] for payment in self.payments if payment['from'] == user)

            balance = per_person_expense - payments_to_user + payments_from_user
            print(f"{user}: {balance}")

        if total_expenses == len(self.users) * per_person_expense:
            print("Trip expenses settled.")
        else:
            print("Trip expenses not settled.")

# Create a new trip expense instance
trip = TripExpense()

# Add expenses
trip.add_expense('A', 100, 'Food')
trip.add_expense('B', 200, 'Accommodation')
trip.add_expense('C', 300, 'Travel')
trip.add_expense('D', 50, 'Food')
trip.add_expense('E', 50, 'Food')

# Upload receipts
trip.upload_receipt('Receipt 1')
trip.upload_receipt('Receipt 2')
trip.upload_receipt('Receipt 3')

# Tag members for expenses
trip.tag_members(0, ['A', 'B', 'C'])
trip.tag_members(3, ['D', 'E'])

# Make payments
trip.make_payment('A', 'B', 50)
trip.make_payment('C', 'A', 100)
trip.make_payment('E', 'D', 25)

# Close the trip and display settlement status
trip.close_trip()
