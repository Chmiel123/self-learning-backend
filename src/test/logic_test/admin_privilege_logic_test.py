from src.logic import admin_privilege_logic
from src.models.account.admin_privilege import AdminPrivilege
from src.models.system.language import Language
from src.test.base_with_context_test import BaseWithContextTest
from src.utils.exceptions import AdminPrivilegeStrengthInvalidException, NotAuthorizedException, \
    AdminPrivilegeNotFoundException


class AdminPrivilegeLogicTest(BaseWithContextTest):
    def setUp(self):
        super().setUp()
        language = Language()
        language.code = 'es'
        language.english_name = 'spanish'
        language.native_name = 'espanol'
        language.save_to_db()

    def test_create_admin_privilege(self):
        admin_privilege_logic.create_or_update({
            "account_id": 2,
            "language_id": 1,
            "strength": 3
        })
        admin_privilege = AdminPrivilege.find_by_account_id_and_language_id(2, 1)
        self.assertEqual(2, admin_privilege.account_id)
        self.assertEqual(1, admin_privilege.language_id)
        self.assertEqual(3, admin_privilege.strength)

    def test_update_admin_privilege(self):
        admin_privilege_logic.create_or_update({
            "account_id": 2,
            "language_id": 1,
            "strength": 3
        })
        admin_privilege = AdminPrivilege.find_by_account_id_and_language_id(2, 1)
        self.assertEqual(2, admin_privilege.account_id)
        self.assertEqual(1, admin_privilege.language_id)
        self.assertEqual(3, admin_privilege.strength)
        admin_privilege_logic.create_or_update({
            "account_id": 2,
            "language_id": 1,
            "strength": 4
        })
        admin_privilege = AdminPrivilege.find_by_account_id_and_language_id(2, 1)
        self.assertEqual(2, admin_privilege.account_id)
        self.assertEqual(1, admin_privilege.language_id)
        self.assertEqual(4, admin_privilege.strength)
        admin_privilege_logic.create_or_update({
            "account_id": 2,
            "language_id": 1,
            "strength": 4
        })
        admin_privilege = AdminPrivilege.find_by_account_id_and_language_id(2, 1)
        self.assertEqual(2, admin_privilege.account_id)
        self.assertEqual(1, admin_privilege.language_id)
        self.assertEqual(4, admin_privilege.strength)

    def test_get_admin_privilege_for_account(self):
        result = admin_privilege_logic.get_admin_privileges_for_account(1)
        self.assertEqual(1, result['admin_privileges'][0]['account_id'])
        self.assertEqual(1, result['admin_privileges'][0]['language_id'])
        self.assertEqual(5, result['admin_privileges'][0]['strength'])

    def test_delete_admin_privilege(self):
        admin_privilege_logic.create_or_update({
            "account_id": 2,
            "language_id": 1,
            "strength": 3
        })
        admin_privilege = AdminPrivilege.find_by_account_id_and_language_id(2, 1)
        self.assertEqual(2, admin_privilege.account_id)
        self.assertEqual(1, admin_privilege.language_id)
        self.assertEqual(3, admin_privilege.strength)
        admin_privilege_logic.delete({
            "account_id": 2,
            "language_id": 1
        })
        admin_privilege = AdminPrivilege.find_by_account_id_and_language_id(2, 1)
        self.assertIsNone(admin_privilege)

    def test_strength_too_low_or_too_high(self):
        self.assertRaises(AdminPrivilegeStrengthInvalidException,
                          admin_privilege_logic.create_or_update, {
                                "account_id": 2,
                                "language_id": 1,
                                "strength": 0
                            })
        self.assertRaises(AdminPrivilegeStrengthInvalidException,
                          admin_privilege_logic.create_or_update, {
                                "account_id": 2,
                                "language_id": 1,
                                "strength": -999
                            })
        self.assertRaises(AdminPrivilegeStrengthInvalidException,
                          admin_privilege_logic.create_or_update, {
                                "account_id": 2,
                                "language_id": 1,
                                "strength": 11
                            })

    def test_current_user_not_authorized(self):
        self.login_as_user()
        self.assertRaises(NotAuthorizedException,
                          admin_privilege_logic.create_or_update, {
                                "account_id": 2,
                                "language_id": 1,
                                "strength": 1
                            })

    def test_not_authorized(self):
        self.assertRaises(NotAuthorizedException,
                          admin_privilege_logic.create_or_update, {
                                "account_id": 2,
                                "language_id": 1,
                                "strength": 10
                            })
        admin_privilege_logic.create_or_update({
            "account_id": 2,
            "language_id": 1,
            "strength": 3
        })
        self.login_as_user()
        self.assertRaises(NotAuthorizedException,
                          admin_privilege_logic.create_or_update, {
                                "account_id": 1,
                                "language_id": 1,
                                "strength": 2
                            })
        self.assertRaises(NotAuthorizedException,
                          admin_privilege_logic.delete, {
                                "account_id": 1,
                                "language_id": 1
                            })

    def test_delete_not_found(self):
        self.assertRaises(AdminPrivilegeNotFoundException,
                          admin_privilege_logic.delete, {
                                "account_id": 3,
                                "language_id": 3
                            })
