import allure
from faker import Faker

from app import app
from models.users import Student

fake = Faker()


def test_submit_student_registration_form():
    student = Student()

    # app.registration_page.open()
    app.left_panel.open_practice_form().register(student)

    # app.registration_page.register(student)

    app.registration_page.should_have_registered(student)

    # table.all("td").should(
    #     have.exact_texts(
    #         ("Student Name", f"{student.first_name} {student.last_name}"),
    #         ("Student Email", "student.email"),
    #         ("Gender", student.gender),
    #         ("Mobile", student.phone_number),
    #         ("Date of Birth", student.date_of_birth.strftime("%d %B,%Y")),
    #         ("Subjects", ", ".join(student.subjects)),
    #         ("Hobbies", ", ".join(student.hobbies)),
    #         ("Picture", formated_picture),
    #         ("Address", student.address),
    #         ("State and City", f"{student.state} {student.city}"),
    #     )
    # )
