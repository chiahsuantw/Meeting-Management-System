from main import db


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    chair_speech = db.Column(db.String)  # TODO: What is the max length?

    # Change attr. name chairman to chair
    # TODO: Meeting-Person relationship
    chair = db.relationship('Person', backref=db.backref('meeting', uselist=False))

    attachments = db.relationship('Attachment', backref='meeting')
    announcements = db.relationship('Announcement', backref='meeting')
    extempores = db.relationship('Extempore', backref='meeting')
    motions = db.relationship('Motion', backref='meeting')


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))  # TODO: How to implement choose field?
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True)  # TODO: Can email be the primary key?
    # Add new attr. type
    type = db.Column(db.String(10), nullable=False)  # TODO: How to implement choose field?

    expert_info = db.relationship('Expert', backref=db.backref('person', uselist=False))
    assistant_info = db.relationship('Assistant', backref=db.backref('person', uselist=False))
    dept_prof_info = db.relationship('DeptProf', backref=db.backref('person', uselist=False))
    other_prof_info = db.relationship('OtherProf', backref=db.backref('person', uselist=False))
    student_info = db.relationship('Student', backref=db.backref('person', uselist=False))


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
    filepath = db.Column(db.String, nullable=False)  # TODO: Should we set length limits?
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))


class Announcement(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))


class Extempore(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))


class Motion(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    status = db.Column(db.String(10))  # TODO: How to implement choose field?
    resolution = db.Column(db.String)
    execution = db.Column(db.String)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))
