from src.util.exceptions import InvalidInputDataException
from src.models.account.account import Account


def find_by_id(id: int) -> Account:
    return Account.find_by_id(id)


def find_by_username(name: str) -> Account:
    return Account.find_by_username(name)


def find_by_email(email: str) -> Account:
    return Account.find_by_email(email)


def create_account_with_password(username: str, email: str, password: str) -> Account:
    if find_by_username(username):
        raise InvalidInputDataException(f'User {username} already exists')
    if find_by_email(email):
        raise InvalidInputDataException(f'User with email {email} already exists')

    #TODO: email goes to account verification entity
    new_account = Account(username, email, password)
    new_account.save_to_db()

    return new_account


def login(username_or_email: str, password: str) -> Account:
    current_account = Account.find_by_username(username_or_email)

    if current_account:
        if Account.verify_hash(password, current_account.password):
            return current_account

    current_account = Account.find_by_email(username_or_email)
    if current_account:
        if Account.verify_hash(password, current_account.password):
            return current_account

    else:
        raise InvalidInputDataException('Wrong credentials.')
