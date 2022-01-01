import json
from os import path

from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required
from sqlalchemy.exc import DataError
from werkzeug.utils import secure_filename

from main import app
from main.models import Person, db, Student, Attachment, Meeting, Announcement, Motion, Extempore


@app.route('/')
@login_required
def home():
    return redirect(url_for('meeting'))


@app.route('/meeting')
@app.route('/meeting/<int:meeting_id>')
@login_required
def meeting(meeting_id=None):
    return render_template('meeting.html', meetings=Meeting.query, selected_meeting_id=meeting_id)


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
    meeting.chair_id = int(data['chair'])
    meeting.minute_taker_id = int(data['minuteTaker'])
    meeting.chair_speech = data['chairSpeech']

    for att_id in data['attendee']:
        person = Person.query.get(int(att_id))
        meeting.attendees.append(person)

    for gue_id in data['guest']:
        person = Person.query.get(int(gue_id))
        meeting.attendees.append(person)
        meeting.attendee_association[-1].is_member = False

    for content in data['announcement']:
        announcement = Announcement(content)
        meeting.announcements.append(announcement)

    for motion_form in data['motion']:
        motion = Motion(motion_form['MotionDescription'],
                        motion_form['MotionContent'],
                        motion_form['MotionStatus'],
                        motion_form['MotionResolution'],
                        motion_form['MotionExecution'])
        meeting.motions.append(motion)

    for content in data['extempore']:
        extempore = Extempore(content)
        meeting.extempores.append(extempore)

    for file in files:
        filename = str(meeting.id) + '-' + secure_filename(file.filename)
        filepath = path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        attachment = Attachment(filename, filepath)
        meeting.attachments.append(attachment)

    db.session.add(meeting)
    db.session.commit()

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
