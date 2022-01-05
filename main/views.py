import json
from os import path

from flask import render_template, redirect, url_for, flash, request, jsonify, send_file, abort
from flask_login import login_user, logout_user, login_required
from sqlalchemy import desc
from sqlalchemy.exc import DataError

from main import app
from main.models import Person, db, Student, Attachment, Meeting, Announcement, Motion, Extempore, Attendee


@app.route('/')
@login_required
def home():
    return redirect(url_for('meeting_page'))


@app.route('/meeting')
@app.route('/meeting/<int:meeting_id>')
@login_required
def meeting_page(meeting_id=None):
    meeting = Meeting.query.get_or_404(meeting_id) if meeting_id else None
    meetings = Meeting.query.order_by(desc(Meeting.time))
    attendees = Attendee.query.filter_by(meeting_id=meeting_id)
    return render_template('meeting.html', meetings=meetings, meeting=meeting, attendees=attendees)


@app.route('/motion')
@login_required
def motion_page():
    motions = Motion.query
    return render_template('motion.html', motions=motions)


@app.route('/person')
@app.route('/person/<int:person_id>')
@login_required
def person_page(person_id=None):
    person = Person.query.get_or_404(person_id) if person_id else None
    people = Person.query
    return render_template('person.html', people=people, person=person)


@app.route('/get/meeting')
@login_required
def meeting_view():
    meeting_id = request.args.get('id')
    if not meeting_id:
        return abort(400)
    meeting = Meeting.query.get_or_404(int(meeting_id))
    attendees = Attendee.query.filter_by(meeting_id=meeting_id)
    return render_template('components/meeting-view.html', meeting=meeting, attendees=attendees)


@app.route('/get/motion')
@login_required
def motion_view():
    motion_id = request.args.get('id')
    if not motion_id:
        return abort(400)
    motion = Motion.query.filter_by(id=motion_id).first_or_404(int(motion_id))
    return render_template('components/motion-view.html', motion=motion)


@app.route('/get/person')
@login_required
def person_view():
    person_id = request.args.get('id')
    if not person_id:
        return abort(400)
    person = Person.query.get_or_404(int(person_id))
    return render_template('components/person-view.html', person=person)


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

    print(data)
    print(data['present'])

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

    attendees = Attendee.query.filter_by(meeting_id=meeting.id)

    present = data['present']
    for attendee in attendees:
        if attendee.person_id in present:
            attendee.is_present = True
        else:
            attendee.is_present = False

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
        # secure_filename() does not allow Chinese characters
        filename = str(meeting.id) + '-' + file.filename
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


@app.route('/edit/meeting/<int:meeting_id>')
def edit_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(int(meeting_id))
    return render_template('edit-meeting.html', meeting=meeting)


@app.route('/uploads/<int:file_id>', methods=['GET', 'POST'])
def download(file_id):
    file = Attachment.query.filter_by(id=file_id).first()
    return send_file(path_or_file=file.file_path, as_attachment=False,
                     download_name=file.filename.split('-', 1)[1])


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
