from src.models.account.account import Account
from src.models.content.category import Category
from src.models.content.category_course_link import CategoryCourseLink
from src.models.content.course import Course
from src.models.system.entity_status import EntityStatus
from src.models.system.language import Language

list_of_courses = [
    ['Geometry 101', 'This is a great course', 5, EntityStatus.active, 150, 11, ],
    ['Geometry 102', 'This is a great course', 5, EntityStatus.active, 78, 21, ],
    ['Calculus 101', 'This is a great course', 6, EntityStatus.draft, 78, 21, ]
]
lang = Language.find_by_code('en')
account = Account.find_by_username('john')
for lg in list_of_courses:
    course = Course()
    course.author_id = account.id
    course.name = lg[0]
    course.content = lg[1]
    course.language_id = lang.id
    course.status = lg[3]
    course.likes = lg[4]
    course.dislikes = lg[5]
    course.save_to_db()
    category_course_link = CategoryCourseLink(lg[2], course.id)
    category_course_link.save_to_db()
    if course.status == EntityStatus.active:
        category = Category.find_by_id(category_course_link.category_id)
        category.nr_active_courses += 1
        category.save_to_db()
