from flask import Flask, render_template, request

app = Flask(__name__)

# Sample data
users = ['A', 'B', 'C', 'D', 'E']
expenses = []
payments = []
receipts = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_expense', methods=['POST'])
def add_expense():
    user = request.form.get('user')
    amount = float(request.form.get('amount'))
    description = request.form.get('description')

    expenses.append({'user': user, 'amount': amount, 'description': description})
    return 'Expense added successfully'


@app.route('/upload_receipt', methods=['POST'])
def upload_receipt():
    receipt = request.files['receipt']
    receipts.append(receipt.filename)
    receipt.save(receipt.filename)
    return 'Receipt uploaded successfully'


@app.route('/tag_members', methods=['POST'])
def tag_members():
    expense_index = int(request.form.get('expense_index'))
    members = request.form.getlist('members[]')

    if expense_index < len(expenses):
        expenses[expense_index]['members'] = members

    return 'Members tagged successfully'


@app.route('/make_payment', methods=['POST'])
def make_payment():
    from_user = request.form.get('from_user')
    to_user = request.form.get('to_user')
    amount = float(request.form.get('amount'))

    payments.append({'from': from_user, 'to': to_user, 'amount': amount})
    return 'Payment made successfully'


@app.route('/close_trip')
def close_trip():
    total_expenses = sum(expense['amount'] for expense in expenses)
    per_person_expense = total_expenses / len(users)

    settlements = {}

    for user in users:
        payments_to_user = sum(payment['amount'] for payment in payments if payment['to'] == user)
        payments_from_user = sum(payment['amount'] for payment in payments if payment['from'] == user)

        balance = per_person_expense - payments_to_user + payments_from_user
        settlements[user] = balance

    if total_expenses == len(users) * per_person_expense:
        status = "Trip expenses settled."
    else:
        status = "Trip expenses not settled."

    return render_template('close_trip.html', settlements=settlements, status=status)


if __name__ == '__main__':
    app.run(debug=True)
