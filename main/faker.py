import random
from datetime import datetime

from faker import Faker

from main import db
from main.models import Meeting, MeetingType, Person, PersonType, GenderType

faker = Faker('zh_TW')


def add_meetings(num):
    for i in range(num):
        meeting = Meeting()
        meeting.title = '會議 ' + str(random.randint(0, 100))
        meeting.type = MeetingType.DeptAffairs
        meeting.time = datetime.utcnow()
        meeting.location = faker.address()
        meeting.chair_speech = faker.text()
        db.session.add(meeting)
    db.session.commit()


def add_people(num):
    for i in range(num):
        person = Person()
        person.name = faker.name()
        person.gender = GenderType.Male
        person.phone = faker.phone_number()
        person.email = faker.email()
        person.type = PersonType.Student
        db.session.add(person)
    db.session.commit()
