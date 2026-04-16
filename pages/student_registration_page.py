from datetime import date

import allure
from selene import browser, have, be, command
import re

from models.users import Student, HOBBIES


class StudentRegistrationPage:

    def __init__(self):
        self.first_name = browser.element("#firstName")
        self.last_name = browser.element("#lastName")
        self.email = browser.element("#userEmail")
        self.gender = browser.all("[name='gender']")
        self.number = browser.element("#userNumber")

        self.date_of_birth_input = browser.element("#dateOfBirthInput")
        self.date_of_birth = browser.element("#dateOfBirth")
        self.month_select = self.date_of_birth.element(
            ".react-datepicker__month-select"
        )
        self.year_select = self.date_of_birth.element(".react-datepicker__year-select")

        self.modal_content = browser.element(".modal-content")
        self.table = self.modal_content.element(".table")

    def moth_select_option(self, month: int) -> browser.element:
        return self.month_select.element(f"option[value='{month}']")

    def open(self):
        browser.open("/automation-practice-form")

    @allure.step("Зарегистрировать пользователя {student}")
    def register(self, student: Student):
        self.fill_first_name(student.first_name)
        self.fill_last_name(student.last_name)
        self.fill_email(student.email)
        self.fill_gender(student.gender)
        self.fill_phone_number(student.phone_number)
        self.fill_date_of_birth(student.date_of_birth)

        if student.subjects:  # TODO for unrequited fields
            self.fill_subjects(student.subjects)

        self.fill_hobbies(student.hobbies)
        self.fill_picture(student.picture)
        self.fill_address(student.address)
        self.scroll_to_submit()
        self.fill_state(student.state)
        self.fill_city(student.city)

        self.submit()

    def fill_first_name(self, value: str):
        self.first_name.type(value)

    def fill_last_name(self, value: str):
        self.last_name.type(value)

    def fill_email(self, value: str):
        self.email.type(value)

    def fill_gender(self, value: str):
        self.gender.element_by(have.value(value)).click()

    def fill_phone_number(self, value: str):
        self.number.type(value)

    def fill_date_of_birth(self, date_of_birth: date):
        self.date_of_birth_input.click()
        self.month_select.click()
        self.moth_select_option(date_of_birth.month - 1).click()  # TODO dynamic locator
        self.year_select.click()
        self.year_select.element(f"option[value='{date_of_birth.year}']").click()
        suffix = str(date_of_birth.day).rjust(3, "0")
        self.date_of_birth.element(
            f".react-datepicker__day--{suffix}:not(.react-datepicker__day--outside-month)"
        ).click()

    def fill_subjects(self, subjects: list[str]):
        for index in range(len(subjects)):
            browser.element("#subjectsInput").type(subjects[index])
            browser.element("#subjectsContainer").element(
                "div[class$='-menu']"
            ).element(f"//div[text()='{subjects[index]}']").click()

    def fill_hobbies(self, hobbies: list[str]):
        for hobby in hobbies:
            browser.all("[id^='hobbies-checkbox-']").element_by(
                have.value(HOBBIES[hobby])
            ).click()

    def fill_picture(self, value: str):
        browser.element("#uploadPicture").send_keys(value)

    def fill_address(self, value: str):
        browser.element("#currentAddress").type(value)

    def scroll_to_submit(self):
        browser.element("#submit").perform(command.js.scroll_into_view)

    def fill_state(self, value: str):
        browser.element("#state").click()
        browser.element("#state").element("div[class$='-menu']").element(
            f"//div[text()='{value}']"
        ).click()

    def fill_city(self, value: str):
        browser.element("#city").click()
        browser.element("#city").element("div[class$='-menu']").element(
            f"//div[text()='{value}']"
        ).click()

    def submit(self):
        browser.element("#submit").click()

    def should_have_registered(self, student: Student):
        self.modal_content.should(be.visible)

        self.assert_full_name(student.first_name, student.last_name)
        self.assert_email(student.email)
        self.assert_gender(student.gender)
        self.assert_phone_number(student.phone_number)
        self.assert_date_of_birth(student.date_of_birth)

        if student.subjects:  # TODO for unrequired fields
            self.assert_subjects(student.subjects)

        self.assert_hobbies(student.hobbies)
        self.assert_picture(student.picture)
        self.assert_address(student.address)
        self.assert_state_city(student.state, student.city)

    def assert_full_name(self, first_name: str, last_name: str):
        self.table.element("//td[text()='Student Name']/following-sibling::td").should(
            have.text(f"{first_name} {last_name}")
        )

    def assert_email(self, email: str):
        self.table.element("//td[text()='Student Email']/following-sibling::td").should(
            have.text(email)
        )

    def assert_gender(self, gender: str):
        self.table.element("//td[text()='Gender']/following-sibling::td").should(
            have.text(gender)
        )

    def assert_phone_number(self, phone_number: str):
        self.table.element("//td[text()='Mobile']/following-sibling::td").should(
            have.text(phone_number)
        )

    def assert_date_of_birth(self, date_of_birth: date):
        self.table.element("//td[text()='Date of Birth']/following-sibling::td").should(
            have.text(date_of_birth.strftime("%d %B,%Y"))
        )

    def assert_subjects(self, subjects: list[str]):
        self.table.element("//td[text()='Subjects']/following-sibling::td").should(
            have.text(", ".join(subjects))
        )

    def assert_hobbies(self, hobbies: list[str]):
        self.table.element("//td[text()='Hobbies']/following-sibling::td").should(
            have.text(", ".join(hobbies))
        )

    def assert_picture(self, picture: str):
        formated_picture, *_ = re.findall(r"(\w+\.\w+)$", picture)
        formated_picture, *_ = re.findall(r"(\w+\.\w+)$", picture)
        self.table.element("//td[text()='Picture']/following-sibling::td").should(
            have.text(formated_picture)
        )

    def assert_address(self, address: str):
        self.table.element("//td[text()='Address']/following-sibling::td").should(
            have.text(address)
        )

    def assert_state_city(self, state: str, city: str):
        self.table.element(
            "//td[text()='State and City']/following-sibling::td"
        ).should(have.text(f"{state} {city}"))
