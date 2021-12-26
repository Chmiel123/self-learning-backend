from src.models.account.account import Account


new_account = Account("john", "pass")
new_account.email = "john@example.com"
new_account.save_to_db()

new_account = Account("bill", "pass")
new_account.email = "bill@example.com"
new_account.save_to_db()
