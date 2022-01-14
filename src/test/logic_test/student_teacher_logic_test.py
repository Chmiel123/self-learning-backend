from src.logic import student_teacher_logic, account_logic
from src.models.account.account import Account
from src.models.account.student_teacher_link import StudentTeacherLink
from src.models.account.student_teacher_request import StudentTeacherRequest
from src.test.base_with_context_test import BaseWithContextTest
from src.utils.exceptions import NotAuthorizedException, StudentTeacherLinkAlreadyExistException, \
    StudentTeacherTheSameException


class StudentTeacherLogicTest(BaseWithContextTest):
    def test_make_request(self):
        student_teacher_logic.make_request(1, 2)
        request = StudentTeacherRequest.find_by_teacher_id_and_student_id(1, 2)
        self.assertIsNotNone(request)
        self.assertEqual(1, request.teacher_id)
        self.assertEqual(2, request.student_id)
        self.assertEqual(True, request.teacher_accepted)
        self.assertEqual(False, request.student_accepted)

        self.login_as_user()
        student_teacher_logic.make_request(1, 2)
        request = StudentTeacherRequest.find_by_teacher_id_and_student_id(1, 2)
        self.assertIsNone(request)
        link = StudentTeacherLink.find_by_teacher_id_and_student_id(1, 2)
        self.assertIsNotNone(link)
        self.assertEqual(1, link.teacher_id)
        self.assertEqual(2, link.student_id)

        self.assertRaises(StudentTeacherLinkAlreadyExistException,
                          student_teacher_logic.make_request, 1, 2)

    def test_remove_request_and_link(self):
        student_teacher_logic.make_request(1, 2)
        self.login_as_user()
        student_teacher_logic.make_request(1, 2)
        link = StudentTeacherLink.find_by_teacher_id_and_student_id(1, 2)
        self.assertIsNotNone(link)
        student_teacher_logic.remove_request_and_link(1, 2)
        link = StudentTeacherLink.find_by_teacher_id_and_student_id(1, 2)
        self.assertIsNone(link)

    def test_are_linked(self):
        are_linked = student_teacher_logic.are_linked(1, 2)
        self.assertEqual(False, are_linked)

        student_teacher_logic.make_request(1, 2)
        self.login_as_user()
        student_teacher_logic.make_request(1, 2)

        are_linked = student_teacher_logic.are_linked(1, 2)
        self.assertEqual(True, are_linked)

    def test_remove_request_and_link_not_authorized(self):
        account_logic.create_account_with_password('jill', 'jill@example.com', 'pass')
        student_teacher_logic.make_request(1, 2)
        self.login_as_user()
        student_teacher_logic.make_request(1, 2)
        self.login_as(Account.find_by_id(3))
        self.assertRaises(NotAuthorizedException, student_teacher_logic.remove_request_and_link, 1, 2)

    def test_student_teacher_same_exception(self):
        self.assertRaises(StudentTeacherTheSameException, student_teacher_logic.make_request, 1, 1)
        self.assertRaises(StudentTeacherTheSameException, student_teacher_logic.remove_request_and_link, 1, 1)
        self.assertRaises(StudentTeacherTheSameException, student_teacher_logic.are_linked, 1, 1)

    def test_get_details(self):
        student_teacher_logic.make_request(1, 2)
        student_teacher_logic.make_request(2, 1)
        self.login_as_user()
        student_teacher_logic.make_request(1, 2)
        student_teacher_logic.make_request(2, 1)
        result = student_teacher_logic.get_details()
        self.assertEqual(1, result['teachers'][0])
        self.assertEqual(1, result['students'][0])