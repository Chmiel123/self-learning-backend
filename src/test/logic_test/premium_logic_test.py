import datetime
from dateutil.relativedelta import relativedelta

from src.logic import premium_logic
from src.models.account.account import Account
from src.models.account.premium_time import PremiumTime
from src.test.base_with_context_test import BaseWithContextTest


class PremiumLogicTest(BaseWithContextTest):
    def test_add_premium_time(self):
        premium_logic.add_premium(1)
        premium_time = PremiumTime.find_by_account_id(1)
        self.assertIsNotNone(premium_time)
        now = datetime.datetime.utcnow()
        then = None
        if now.month == 12:
            then = datetime.datetime(now.year + 1, 1, now.day, now.hour, now.minute, now.second)
        else:
            then = datetime.datetime(now.year, now.month + 1, now.day, now.day, now.hour, now.minute, now.second)

        self.assertAlmostEqual(then, premium_time.end_date, delta=datetime.timedelta(days=1))
        premium_logic.add_premium(1)
        premium_time = PremiumTime.find_by_account_id(1)
        self.assertIsNotNone(premium_time)
        now = datetime.datetime.utcnow()
        then = None
        if now.month >= 11:
            then = datetime.datetime(now.year + 1, now.month - 10, now.day, now.hour, now.minute, now.second)
        else:
            then = datetime.datetime(now.year, now.month + 2, now.day, now.day, now.hour, now.minute, now.second)

        self.assertAlmostEqual(then, premium_time.end_date, delta=datetime.timedelta(days=1))

    def test_is_premium(self):
        is_premium = premium_logic.is_premium(1)
        self.assertEqual(False, is_premium)
        premium_logic.add_premium(1)
        is_premium = premium_logic.is_premium(1)
        self.assertEqual(True, is_premium)
