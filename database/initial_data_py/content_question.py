from src.models.content.lesson import Lesson
from src.models.content.question import Question

questions = [
    ['Question 01', "['A','B','C','D']", "[3]", 1, 6, "Solution"],
    ['Question 02', "['A','B','C','D']", "[3]", 1, 6, "Solution"],
    ['Question 03', "['A','B','C','D']", "[3]", 1, 6, "Solution"],
    ['Question 04', "['A','B','C','D']", "[3]", 1, 6, "Solution"],
    ['Question 05', "['A','B','C','D']", "[3]", 1, 6, "Solution"],
    ['Question 06', "['A','B','C','D']", "[3]", 1, 6, "Solution"],
    ['Question 07', "['A','B','C','D']", "[3]", 1, 6, "Solution"],
    ['Question 08', "['A','B','C','D']", "[3]", 1, 6, "Solution"],
    ['Question 09', "['A','B','C','D']", "[3]", 1, 6, "Solution"],
    ['Question 10', "['A','B','C','D']", "[3]", 1, 6, "Solution"],
    ['Question 11', "['A','B','C','D']", "[3]", 1, 6, "Solution"]
]

lesson = Lesson.find_by_id(6)

for q in questions:
    question = Question()
    question.lesson_id = lesson.id
    question.question = q[0]
    question.available_answers = q[1]
    question.correct_answers = q[2]
    question.order_begin = q[3]
    question.order_end = q[4]
    question.solution = q[5]
    question.save_to_db()
