from selene import browser, have, be, command

from pages.student_registration_page import StudentRegistrationPage


class LeftPanelPage:
    def __init__(self):
        self.left_panel = browser.element(".left-pannel")
        self.category_cards = browser.element(".category-cards")

    def open_simple_registration_form(self):
        self.open("Elements", "Text Box")

    def open_practice_form(self):
        self.open("Forms", "Practice Form")
        return StudentRegistrationPage()

    def open(self, group: str, item: str):
        browser.open("/")
        self.category_cards.element(f"//*[text()='{group}']").click()
        self.left_panel.element(".element-list.show").element(f"//*[text()='{item}']").click()
