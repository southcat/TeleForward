from config import db


accounts = db.get_accounts_by_phone_number("+19513668666")
account_id,phone_number,session_string = accounts[0]
print(account_id)