import random

from faker import Faker

from main.models import *

faker = Faker('zh_TW')


def add_meetings(num):
    for i in range(num):
        person = Person.query.all()
        random.shuffle(person)

        meeting = Meeting()
        meeting.title = '會議 ' + str(faker.pyint())
        meeting.type = random.choice(list(MeetingType))
        meeting.time = datetime.utcnow()
        meeting.location = faker.address()
        meeting.chair = person.pop()
        meeting.chair_speech = faker.text()
        meeting.minute_taker = person.pop()
        for _ in range(random.randrange(2, len(person))):
            meeting.attendees.append(person.pop())
            meeting.attendee_association[-1].is_member = bool(random.getrandbits(1))
            meeting.attendee_association[-1].is_present = bool(random.getrandbits(1))

        for _ in range(random.randint(0, 5)):
            meeting.announcements.append(generate_announcement())

        for _ in range(random.randint(1, 3)):
            meeting.motions.append(generate_motion())

        for _ in range(random.randint(0, 3)):
            meeting.extempores.append(generate_extempore())

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
        if person.type.name == 'Expert':
            person.expert_info = generate_expert()
        elif person.type.name == 'Assistant':
            person.assistant_info = generate_assistant()
        elif person.type.name == 'DeptProf':
            person.dept_prof_info = generate_dept_prof()
        elif person.type.name == 'OtherProf':
            person.other_prof_info = generate_other_prof()
        elif person.type.name == 'Student':
            person.student_info = generate_student()

        db.session.add(person)
    db.session.commit()


def generate_other_prof():
    other_prof = OtherProf()
    other_prof.univ_name = "高雄大學"
    other_prof.address = faker.address()
    other_prof.office_tel = faker.phone_number()
    other_prof.job_title = faker.job()
    other_prof.bank_account = faker.isbn10()
    other_prof.dept_name = faker.license_plate()
    return other_prof


def generate_dept_prof():
    dept_prof = DeptProf()
    dept_prof.job_title = faker.job()
    dept_prof.office_tel = faker.phone_number()
    return dept_prof


def generate_expert():
    expert = Expert()
    expert.office_tel = faker.phone_number()
    expert.company_name = faker.company()
    expert.address = faker.address()
    expert.job_title = faker.job()
    expert.bank_account = faker.isbn10()
    return expert


def generate_assistant():
    assistant = Assistant()
    assistant.office_tel = faker.phone_number()
    return assistant


def generate_student():
    student = Student()
    student.student_id = 'A' + str(random.randint(100, 115)) + str(random.randint(1000, 9999))
    student.program = random.choice(list(StudentProgramType))
    student.study_year = random.choice(list(StudentStudyYearType))
    return student


def generate_announcement():
    announcement = Announcement(
        content=faker.paragraph(nb_sentences=random.randint(3, 5)))
    return announcement


def generate_motion():
    motion = Motion(description=faker.sentence(),
                    content=faker.paragraph(nb_sentences=random.randint(0, 5)),
                    status=random.choice(list(MotionStatusType)),
                    resolution=faker.paragraph(nb_sentences=random.randint(0, 3)),
                    execution=faker.paragraph(nb_sentences=random.randint(0, 3))
                    )
    return motion


def generate_extempore():
    extempore = Extempore(
        content=faker.paragraph(nb_sentences=random.randint(3, 5)))
    return extempore
