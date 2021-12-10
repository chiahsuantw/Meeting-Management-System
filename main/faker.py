import random

from faker import Faker

from main.models import *

faker = Faker('zh_TW')


def add_meetings(num):
    for i in range(num):
        meeting = Meeting()
        meeting.title = '會議 ' + str(faker.pyint())
        meeting.type = random.choice(list(MeetingType))
        meeting.time = datetime.utcnow()
        meeting.location = faker.address()
        meeting.chair_speech = faker.text()
        db.session.add(meeting)
    db.session.commit()


def add_people(num):
    for i in range(num):
        person = Person()
        person.name = faker.name()
        person.gender = random.choice(list(GenderType))
        person.phone = faker.phone_number()
        person.email = faker.email()
        person.type = random.choice(list(PersonType))
        db.session.add(person)
    db.session.commit()


def generate_student():
    student = Student()
    student.student_id = 'A108' + str(random.randint(1000, 9999))
    student.program = random.choice(list(StudentProgramType))
    student.study_year = random.choice(list(StudentStudyYearType))
    return student


def generate_motion():
    motion = Motion()
    motion.description = faker.sentence()
    motion.type = random.choice(list(MotionStatusType))
    return motion
