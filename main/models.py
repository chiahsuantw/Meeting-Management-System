from datetime import datetime
from enum import Enum

from sqlalchemy.ext.associationproxy import association_proxy

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
    # 系務會議
    DeptAffairs = 'DeptAffairs'
    # 系教評會
    FacultyEvaluation = 'FacultyEvaluation'
    # 系課程委員會
    DeptCurriculum = 'DeptCurriculum'
    # 招生暨學生事務委員會
    StudentAffairs = 'StudentAffairs'
    # 系發展協會
    DeptDevelopment = 'DeptDevelopment'
    # 其他
    Other = 'Other'


class StudentProgramType(Enum):
    UnderGraduate = 'UnderGraduate'
    Graduate = 'Graduate'
    PhD = 'PhD'


class StudentStudyYearType(Enum):
    FirstYear = 'FirstYear'
    SecondYear = 'SecondYear'
    ThirdYear = 'ThirdYear'
    ForthYear = 'ForthYear'
    FifthYear = 'FifthYear'
    SixthYear = 'SixthYear'
    SeventhYear = 'SeventhYear'


class MotionStatusType(Enum):
    InDiscussion = 'InDiscussion'
    InExecution = 'InExecution'
    Closed = 'Closed'


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.Enum(MeetingType), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    location = db.Column(db.String(50), nullable=False)
    chair_speech = db.Column(db.Text)

    attachments = db.relationship('Attachment', backref='meeting')
    announcements = db.relationship('Announcement', backref='meeting')
    extempores = db.relationship('Extempore', backref='meeting')
    motions = db.relationship('Motion', backref='meeting')

    # Change attr. name chairman to chair
    chair = association_proxy('chair_association', 'chair')
    minute_takers = association_proxy('minute_taker_association', 'minute_taker')
    attendees = association_proxy('attendee_association', 'attendee')


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.Enum(GenderType), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    # Add new attr. type
    type = db.Column(db.Enum(PersonType), nullable=False)

    expert_info = db.relationship('Expert', backref='basic_info', uselist=False)
    assistant_info = db.relationship('Assistant', backref='basic_info', uselist=False)
    dept_prof_info = db.relationship('DeptProf', backref='basic_info', uselist=False)
    other_prof_info = db.relationship('OtherProf', backref='basic_info', uselist=False)
    student_info = db.relationship('Student', backref='basic_info', uselist=False)

    meetings_as_chair = association_proxy('chair_association', 'meeting')
    meetings_as_minute_taker = association_proxy('minute_taker_association', 'meeting')
    meetings_as_attendee = association_proxy('attendee_association', 'meeting')


class Chair(db.Model):
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    meeting = db.relationship(Meeting, backref='chair_association')
    chair = db.relationship(Person, backref='chair_association')
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)


class MinuteTaker(db.Model):
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    meeting = db.relationship(Meeting, backref='minute_taker_association')
    minute_taker = db.relationship(Person, backref='minute_taker_association')


class Attendee(db.Model):
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    meeting = db.relationship(Meeting, backref='attendee_association')
    attendee = db.relationship(Person, backref='attendee_association')
    is_present = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)


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
    program = db.Column(db.Enum(StudentProgramType), nullable=False)
    # TODO: Should we use constant value instead of study_year?
    study_year = db.Column(db.Enum(StudentStudyYearType), nullable=False)


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
    content = db.Column(db.Text)
    status = db.Column(db.Enum(MotionStatusType))
    resolution = db.Column(db.Text)
    execution = db.Column(db.Text)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))
