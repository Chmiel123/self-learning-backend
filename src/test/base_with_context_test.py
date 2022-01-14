from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, verify_jwt_in_request

from src.logic import account_logic
from src.models.account.account import Account
from src.models.account.admin_privilege import AdminPrivilege
from src.models.system.language import Language
from src.test.base_test import BaseTest


class BaseWithContextTest(BaseTest):
    def setUp(self):
        super().setUp()
        account_logic.create_account_with_password('john', 'john@example.com', 'pass')
        account_logic.create_account_with_password('bill', 'bill@example.com', 'pass')
        language = Language()
        language.code = 'en'
        language.english_name = 'english'
        language.native_name = 'english'
        language.save_to_db()
        admin_privilege = AdminPrivilege()
        admin_privilege.account_id = 1
        admin_privilege.language_id = 1
        admin_privilege.strength = 5
        admin_privilege.save_to_db()
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'secret'
        self.app.config['JWT_SECRET_KEY'] = 'secret'
        JWTManager(self.app)
        self.login_as_admin()

    def tearDown(self):
        self.c.pop()

    def login_as_admin(self):
        self.c = self.app.test_request_context()
        self.c.push()
        access_token = create_access_token(identity="john", expires_delta=False, fresh=True)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        self.c.request.headers = headers
        verify_jwt_in_request()

    def login_as_user(self):
        self.c = self.app.test_request_context()
        self.c.push()
        access_token = create_access_token(identity="bill", expires_delta=False, fresh=True)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        self.c.request.headers = headers
        verify_jwt_in_request()

    def login_as(self, account: Account):
        self.c = self.app.test_request_context()
        self.c.push()
        access_token = create_access_token(identity=account.name, expires_delta=False, fresh=True)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        self.c.request.headers = headers
        verify_jwt_in_request()
