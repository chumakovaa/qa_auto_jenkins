import calendar

from dataclasses import dataclass, field
import os
import random
from datetime import date

from faker import Faker

from pathlib import Path

fake = Faker()

MIN_YEAR = 1970
MAX_YEAR = 2025
MAX_LENGTH_NUMBER = 10

GENDERS = ["Female", "Male", "Other"]
HOBBIES = {"Sports": "1", "Reading": "2", "Music": "3"}
REGIONS = {
    "NCR": ["Delhi", "Gurgaon", "Noida"],
    "Uttar Pradesh": ["Agra", "Lucknow", "Merrut"],
    "Haryana": ["Karnal", "Panipat"],
    "Rajasthan": ["Jaipur", "Jaiselmer"],
}
SUBJECTS = [
    "Hindi",
    "English",
    "Maths",
    "Physics",
    "Chemistry",
    "Biology",
    "Computer Science",
    "Commerce",
    "Accounting",
    "Economics",
    "Arts",
    "Social Studies",
    "History",
    "Civics",
]

def get_random_date(min_year=MIN_YEAR, max_year=MAX_YEAR) -> date:
    year = random.randint(min_year, max_year)
    month = random.randint(1, 12)
    _, total = calendar.monthrange(year, month)
    day = random.randint(1, total)
    return date(year, month, day)


def path(file_name):
    return str(Path(__file__).parent.parent.joinpath(file_name))


def get_random_file(directory="tests/documents/images") -> str:
    images = os.listdir(path(directory))
    image = random.choice(images)
    return path(f"{directory}/{image}")


@dataclass
class Student:
    first_name: str = field(default_factory=fake.first_name)
    last_name: str = field(default_factory=fake.last_name)
    email: str = field(default_factory=fake.email)
    gender: str = field(default_factory=lambda: random.choice(GENDERS))
    phone_number: str = field(
        default_factory=lambda: fake.numerify("#" * MAX_LENGTH_NUMBER)
    )
    date_of_birth: date = field(default_factory=get_random_date)
    subjects: list = field(
        default_factory=lambda: random.sample(
            SUBJECTS, random.randint(1, len(SUBJECTS))
        )
    )
    hobbies: list = field(
        default_factory=lambda: random.sample(
            list(HOBBIES), random.randint(1, len(HOBBIES))
        )
    )
    picture: str = field(default_factory=get_random_file)
    address: str = field(default_factory=lambda: fake.address().replace("\n", " "))
    state: str = field(default_factory=lambda: random.choice(list(REGIONS)))
    city: str = None

    def __post_init__(self):
        if self.city is None:
            self.city = random.choice(REGIONS[self.state])

        with open(path("tests/log.txt"), "w") as file:
            file.write(repr(self))

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"