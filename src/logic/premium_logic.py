import datetime
from dateutil.relativedelta import relativedelta

from src.models.account.premium_time import PremiumTime


def is_premium(account_id: int):
    premium_time = PremiumTime.find_by_account_id(account_id)
    if premium_time and premium_time.end_date >= datetime.datetime.utcnow():
        return True
    return False


def add_premium(account_id: int, months: int = 1):
    premium_time = PremiumTime.find_by_account_id(account_id)
    if premium_time:
        premium_time.end_date = premium_time.end_date + relativedelta(months=months)
    else:
        premium_time = PremiumTime()
        premium_time.account_id = account_id
        premium_time.end_date = datetime.datetime.utcnow() + relativedelta(months=months)
    premium_time.save_to_db()
