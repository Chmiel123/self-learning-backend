from src.logic import account_logic
from src.models.account.student_teacher_link import StudentTeacherLink
from src.models.account.student_teacher_request import StudentTeacherRequest
from src.utils.exceptions import StudentTeacherLinkAlreadyExistException, \
    NotAuthorizedException, InvalidInputDataException, StudentTeacherTheSameException


def are_linked(teacher_id: int, student_id: int):
    if teacher_id == student_id:
        raise StudentTeacherTheSameException()
    existing_link = StudentTeacherLink.find_by_teacher_id_and_student_id(teacher_id, student_id)
    if existing_link:
        return True
    return False


def make_request(teacher_id: int, student_id: int, teacher_accepted: bool, student_accepted: bool):
    if teacher_id == student_id:
        raise StudentTeacherTheSameException()
    existing_link = StudentTeacherLink.find_by_teacher_id_and_student_id(teacher_id, student_id)
    if existing_link:
        raise StudentTeacherLinkAlreadyExistException()
    current_account = account_logic.get_current_account()
    request = StudentTeacherRequest.find_by_teacher_id_and_student_id(teacher_id, student_id)
    if not request:
        request = StudentTeacherRequest()
        request.teacher_id = teacher_id
        request.student_id = student_id
    if teacher_accepted and not request.teacher_accepted:
        if current_account.id == teacher_id:
            request.teacher_accepted = True
        else:
            raise NotAuthorizedException()
    if student_accepted and not request.student_accepted:
        if current_account.id == student_id:
            request.student_accepted = True
        else:
            raise NotAuthorizedException()
    if request.student_accepted and request.teacher_accepted:
        StudentTeacherRequest.delete_by_teacher_id_and_student_id(teacher_id, student_id)
        link = StudentTeacherLink()
        link.teacher_id = teacher_id
        link.student_id = student_id
        link.save_to_db()
    else:
        request.save_to_db()


def remove_request_and_link(teacher_id: int, student_id: int):
    if teacher_id == student_id:
        raise StudentTeacherTheSameException()
    current_account = account_logic.get_current_account()
    if current_account.id != teacher_id and current_account.id != student_id:
        raise NotAuthorizedException()
    StudentTeacherLink.delete_by_teacher_id_and_student_id(teacher_id, student_id)
    StudentTeacherRequest.delete_by_teacher_id_and_student_id(teacher_id, student_id)
