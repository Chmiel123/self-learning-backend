from src.models.account.account import Account
from src.models.content.lesson import Lesson
from src.models.system.entity_status import EntityStatus
from src.models.system.language import Language
from src.models.system.lesson_type import LessonType

lessons = [
    ['lesson 01', 'A line is a line', 14, 2, EntityStatus.active, LessonType.lesson],
    ['lesson 02', 'A square is a square', 14, 2, EntityStatus.active, LessonType.lesson],
    ['lesson 03', 'A triangle is a triangle', 14, 2, EntityStatus.active, LessonType.lesson],
    ['lesson 04', 'A pentagon is a pentagon', 14, 2, EntityStatus.active, LessonType.lesson],
    ['lesson 05', 'A hexagon is a hexagon', 14, 2, EntityStatus.active, LessonType.lesson],
    ['Quiz 01', 'Test your knowledge', 14, 2, EntityStatus.active, LessonType.test],
    ['lesson 06', 'Perpendicular is like this -|', 14, 2, EntityStatus.active, LessonType.lesson],
    ['lesson 07', 'Parallel is like this ||', 14, 2, EntityStatus.active, LessonType.lesson],
    ['Quiz 02', 'Test your knowledge', 14, 2, EntityStatus.active, LessonType.test]
]

lang = Language.find_by_code('en')
account = Account.find_by_username('john')

for index, l in enumerate(lessons):
    lesson = Lesson()
    lesson.course_id = 1
    lesson.name = l[0]
    lesson.content = l[1]
    lesson.likes = l[2]
    lesson.dislikes = l[3]
    lesson.status = l[4]
    lesson.type = l[5]
    lesson.order = index
    lesson.language_id = lang.id
    lesson.author_id = account.id
    lesson.save_to_db()
