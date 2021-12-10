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

    attachments = db.relationship('Attachment', backref='meeting', cascade='all, delete-orphan')
    announcements = db.relationship('Announcement', backref='meeting', cascade='all, delete-orphan')
    extempores = db.relationship('Extempore', backref='meeting', cascade='all, delete-orphan')
    motions = db.relationship('Motion', backref='meeting', cascade='all, delete-orphan')

    # Change attr. name chairman to chair
    chair_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    chair_speech = db.Column(db.Text)
    chair_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    minute_takers = association_proxy('minute_taker_association', 'minute_taker')
    attendees = association_proxy('attendee_association', 'attendee')

    def __repr__(self):
        return f'<Meeting {self.id} {self.title} {self.type.value}>'

    def minute_takers_filter_by(self, **kwargs):
        return Person.query.filter_by(**kwargs).join(MinuteTaker).join(Meeting).filter_by(id=self.id)

    def attendees_filter_by(self, **kwargs):
        return Person.query.filter_by(**kwargs).join(Attendee).join(Meeting).filter_by(id=self.id)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.Enum(GenderType), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    # Add new attr. type
    type = db.Column(db.Enum(PersonType), nullable=False)

    # TODO: type constraint to person_type_info
    expert_info = db.relationship('Expert', backref='basic_info', uselist=False, cascade='all, delete-orphan')
    assistant_info = db.relationship('Assistant', backref='basic_info', uselist=False, cascade='all, delete-orphan')
    dept_prof_info = db.relationship('DeptProf', backref='basic_info', uselist=False, cascade='all, delete-orphan')
    other_prof_info = db.relationship('OtherProf', backref='basic_info', uselist=False, cascade='all, delete-orphan')
    student_info = db.relationship('Student', backref='basic_info', uselist=False, cascade='all, delete-orphan')

    meetings_as_chair = db.relationship('Meeting', backref='chair')
    meetings_as_minute_taker = association_proxy('minute_taker_association', 'meeting')
    meetings_as_attendee = association_proxy('attendee_association', 'meeting')

    def __repr__(self):
        return f'<Person {self.id} {self.name} {self.type.value}>'


class MinuteTaker(db.Model):
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    meeting = db.relationship(Meeting, backref='minute_taker_association')
    minute_taker = db.relationship(Person, backref='minute_taker_association')

    def __repr__(self):
        return f'<MinuteTaker {self.meeting.title} {self.minute_taker.name}>'


class Attendee(db.Model):
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    meeting = db.relationship(Meeting, backref='attendee_association')
    attendee = db.relationship(Person, backref='attendee_association')
    is_present = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    is_member = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f'<Attendee {self.meeting.title} {self.attendee.name}>'


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
    student_id = db.Column(db.String(50), nullable=False, unique=True)
    program = db.Column(db.Enum(StudentProgramType), nullable=False)
    study_year = db.Column(db.Enum(StudentStudyYearType), nullable=False)


class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(100), nullable=False)


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
    content = db.Column(db.Text, nullable=False)


class Extempore(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
    content = db.Column(db.Text, nullable=False)


class Motion(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text)
    status = db.Column(db.Enum(MotionStatusType), nullable=False, default=MotionStatusType.InDiscussion)
    resolution = db.Column(db.Text)
    execution = db.Column(db.Text)
