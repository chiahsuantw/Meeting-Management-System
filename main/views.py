import json
from os import path

from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required
from sqlalchemy.exc import DataError
from werkzeug.utils import secure_filename

from main import app
from main.models import Person, db, Student, Attachment, Meeting, Attendee, Announcement


@app.route('/')
@login_required
def home():
    return render_template('meeting.html')


@app.route('/new')
@login_required
def create():
    people = Person.query.all()
    return render_template('create.html', people=people)


@app.route('/new/meeting', methods=['POST'])
@login_required
def new_meeting():
    form = request.form
    data = json.loads(form['json_form'])
    files = request.files.getlist('files[]')

    meeting = Meeting()
    meeting.title = data['title']
    meeting.time = data['time']
    meeting.location = data['location']
    meeting.type = data['type']
    meeting.minute_taker = int(data['minuteTaker'])

    for att_id in data['attendee']:
        meeting.attendees.append(Attendee(int(att_id), True))

    for gue_id in data['guest']:
        meeting.attendees.append(Attendee(int(gue_id), False))
    meeting.chair_speech = int(data['chairSpeech'])

    for ann in data['announcement']:
        meeting.announcements.append(Announcement(ann))

    for file in files:
        filename = secure_filename(file.filename)
        filepath = path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        attachment = Attachment(filename, filepath)
        meeting.attachments.append(attachment)

    # commit point

    # print(meeting.attachments)

    return jsonify({'message': 'Success'})


@app.route('/new/person', methods=['POST'])
@login_required
def new_person():
    form = request.form

    if Person.query.filter_by(email=form['email']).first():
        return jsonify({'message': 'Person already exists'})

    person = Person()
    person.name = form['name']
    person.gender = form['gender']
    person.phone = form['phone']
    person.email = form['email']
    person.type = form['type']

    if person.type == 'DeptProf':
        person.add_dept_prof_info(
            job_title=form['jobTitle'],
            office_tel=form['officeTel']
        )
    elif person.type == 'Assistant':
        person.add_assistant_info(
            office_tel=form['officeTel']
        )
    elif person.type == 'OtherProf':
        person.add_other_prof_info(
            univ_name=form['univName'],
            dept_name=form['deptName'],
            job_title=form['jobTitle'],
            office_tel=form['officeTel'],
            address=form['address'],
            bank_account=form['bankAccount']
        )
    elif person.type == 'Expert':
        person.add_expert_info(
            company_name=form['companyName'],
            job_title=form['jobTitle'],
            office_tel=form['officeTel'],
            address=form['address'],
            bank_account=form['bankAccount']
        )
    elif person.type == 'Student':
        if Student.query.filter_by(student_id=form['studentId']).first():
            return jsonify({'message': 'Student ID already exists'})
        person.add_student_info(
            student_id=form['studentId'],
            program=form['program'],
            study_year=form['studyYear']
        )

    try:
        db.session.add(person)
        db.session.commit()
    except DataError:
        return jsonify({'message': 'Error'})
    finally:
        return jsonify({'message': 'Success',
                        'person': {'id': person.id, 'name': person.name,
                                   'email': person.email, 'type': person.type.value}})


@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    if email:
        user = Person.query.filter_by(email=email).first()
        if user:
            login_user(user, remember=True)
            return redirect(url_for('home'))
        else:
            flash('登入資訊不正確，請再試一次', 'danger')

    return render_template('login.html', title='登入')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
