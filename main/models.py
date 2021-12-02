from main import db


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    chair_speech = db.Column(db.String)  # TODO: What is the max length?


class Person(db.Model):
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))  # TODO: How to implement choose field?
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), primary_key=True)  # TODO: Can email be the primary key?


class Attachment(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String, nullable=False)  # TODO: Should we set length limits?


class Announcement(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)


class Extempore(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)


class Motion(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    status = db.Column(db.String(10))  # TODO: How to implement choose field?
    resolution = db.Column(db.String)
    execution = db.Column(db.String)
