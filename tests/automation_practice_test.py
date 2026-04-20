from app import app
from models.users import Student


def test_submit_student_registration_form():
    student = Student()
    app.left_panel.open_practice_form().register(student)


def test_submit_student_registration_form2():
    student = Student()

    app.left_panel.open_practice_form().register(student)

    app.registration_page.should_have_registered(student)
