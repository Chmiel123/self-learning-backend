import unittest
from src.services import services

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.db = services.db
        services.flask.testing = True
        self.app = services.flask.test_client()
        self.db.session.commit()
        self.db.create_db()
        self.db.session.commit()

        self.users = []

    def tearDown(self):
        pass
