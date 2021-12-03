from enum import Enum

from main import db


class GenderType(Enum):
    Male = 'Male'
    Female = 'Female'


class PersonType(Enum):
    Expert = 'Expert'
    Assistant = 'Assistant'
    DeptProf = 'DeptProf'
    OtherProf = 'OtherProf'
    Student = 'Student'


class MeetingType(Enum):
    pass


class MotionStatusType(Enum):
    pass


# minute_takers = db.Table(
#     'minute_taker',
#     db.Column('person_id', db.Integer, db.ForeignKey('person.id'), primary_key=True),
#     db.Column('meeting_id', db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
# )
#
# attendees = db.Table(
#     'attendee',
#     db.Column('person_id', db.Integer, db.ForeignKey('person.id'), primary_key=True),
#     db.Column('meeting_id', db.Integer, db.ForeignKey('meeting.id'), primary_key=True),
#     db.Column('is_present', db.Boolean),
#     db.Column('is_confirmed', db.Boolean)
# )


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    # date = db.Column(db.Date, nullable=False)
    # time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    chair_speech = db.Column(db.Text)

    # Change attr. name chairman to chair
    # TODO: Meeting-Person relationship
    # chair = db.relationship('Person', backref=db.backref('meeting', uselist=False))
    # minute_takers = db.relationship('Person', secondary=minute_takers, lazy='subquery',
    #                                 backref=db.backref('meetings_as_minute_taker', lazy=True))
    # attendees = db.relationship('Person', secondary=attendees, lazy='subquery',
    #                             backref=db.backref('meetings_as_attendee', lazy=True))

    minute_takers = db.relationship('MinuteTaker', back_populates='meetings_as_minute_taker')
    # attendees = db.relationship('Attendee', back_populates='meetings_as_attendee')

    attachments = db.relationship('Attachment', backref='meeting')
    announcements = db.relationship('Announcement', backref='meeting')
    extempores = db.relationship('Extempore', backref='meeting')
    motions = db.relationship('Motion', backref='meeting')


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.Enum(GenderType))
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True)
    # Add new attr. type
    type = db.Column(db.Enum(PersonType), nullable=False)

    expert_info = db.relationship('Expert', backref='basic_info', uselist=False)
    assistant_info = db.relationship('Assistant', backref='basic_info', uselist=False)
    dept_prof_info = db.relationship('DeptProf', backref='basic_info', uselist=False)
    other_prof_info = db.relationship('OtherProf', backref='basic_info', uselist=False)
    student_info = db.relationship('Student', backref='basic_info', uselist=False)

    meetings_as_minute_taker = db.relationship('MinuteTaker', back_populates='minute_takers')
    # meetings_as_attendee = db.relationship('Attendee', back_populates='attendees')


class MinuteTaker(db.Model):
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
    minute_takers = db.relationship('Person', back_populates='meetings_as_minute_taker')
    meetings_as_minute_taker = db.relationship('Meeting', back_populates='minute_takers')


# class Attendee(db.Model):
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
#     meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
#     is_present = db.Column(db.Boolean)
#     is_confirmed = db.Column(db.Boolean)
#     person = db.relationship('Person', back_populates='attendees')
#     meeting = db.relationship('Meeting', back_populates='meeting')


class Expert(db.Model):
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    company_name = db.Column(db.String(50), nullable=False)
    # Change attr. name from position to job_title
    job_title = db.Column(db.String(50), nullable=False)
    office_tel = db.Column(db.String(20))
    address = db.Column(db.String(500))
    bank_account = db.Column(db.String(50))


class Assistant(db.Model):
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    office_tel = db.Column(db.String(20))


class DeptProf(db.Model):
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    job_title = db.Column(db.String(50), nullable=False)
    office_tel = db.Column(db.String(20))


class OtherProf(db.Model):
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    univ_name = db.Column(db.String(50), nullable=False)
    dept_name = db.Column(db.String(50), nullable=False)
    job_title = db.Column(db.String(50), nullable=False)
    office_tel = db.Column(db.String(20))
    address = db.Column(db.String(500))
    bank_account = db.Column(db.String(50))


class Student(db.Model):
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    student_id = db.Column(db.String(50), nullable=False)
    program = db.Column(db.String(50), nullable=False)
    study_year = db.Column(db.Integer, nullable=False)  # TODO: Should we use constant value instead of study_year?


class Attachment(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String, nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))


class Announcement(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))


class Extempore(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))


class Motion(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(MotionStatusType))
    resolution = db.Column(db.Text)
    execution = db.Column(db.Text)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))
