from pages.left_panel_page import LeftPanelPage
from pages.student_registration_page import StudentRegistrationPage


class ApplicationManager:
    registration_page = StudentRegistrationPage()
    left_panel = LeftPanelPage()

app = ApplicationManager()