import json
from datetime import timedelta
from os import path, remove
from threading import Thread
from time import mktime

from flask import render_template, redirect, url_for, flash, request, jsonify, send_file, abort
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from sqlalchemy import desc, or_
from sqlalchemy.exc import DataError

from main import app, mail
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

    # [Authority Restriction]
    # Do for meetings when at home_page
    if current_user.is_admin():
        meetings = Meeting.query.order_by(desc(Meeting.time))
    else:
        user = Attendee.query.filter_by(person_id=current_user.id)
        meetings_main = Meeting.query.filter(or_(Meeting.chair_id.like(current_user.id),
                                                 Meeting.minute_taker_id.like(current_user.id)))
        meetings = Meeting.query.join(user.subquery()).union(meetings_main).order_by(desc(Meeting.time))

    # [Authority Restriction]
    # Do for meeting at single meeting checkout
    if meeting_id and not current_user.is_admin() and \
            current_user.id != meeting.chair_id and \
            current_user.id != meeting.minute_taker_id and \
            current_user not in meeting.attendees:
        return abort(403)

    attendees = Attendee.query.filter_by(meeting_id=meeting_id)
    return render_template('meeting.html', title='會議列表', meetings=meetings,
                           meeting=meeting, attendees=attendees, timedelta=timedelta)


@app.route('/calendar')
def calendar_page():
    if current_user.is_admin():
        meetings = Meeting.query.order_by(desc(Meeting.time))
    else:
        user = Attendee.query.filter_by(person_id=current_user.id)
        meetings_main = Meeting.query.filter(or_(Meeting.chair_id.like(current_user.id),
                                                 Meeting.minute_taker_id.like(current_user.id)))
        meetings = Meeting.query.join(user.subquery()).union(meetings_main).order_by(desc(Meeting.time))
    return render_template('calendar.html', title='會議行事曆', meetings=meetings)


@app.route('/motion')
@login_required
def motion_page():
    if current_user.is_admin():
        motions = Motion.query.order_by(Motion.status)
    else:
        user = Attendee.query.filter_by(person_id=current_user.id)
        meetings_main = Meeting.query.filter(or_(Meeting.chair_id.like(current_user.id),
                                                 Meeting.minute_taker_id.like(current_user.id)))
        meetings = Meeting.query.join(user.subquery()).union(meetings_main).order_by(desc(Meeting.time))
        motions = Motion.query.join(meetings.subquery()).order_by(Motion.status)

    return render_template('motion.html', title='決策追蹤', motions=motions)


@app.route('/person')
@app.route('/person/<int:person_id>')
@login_required
def person_page(person_id=None):
    person = Person.query.get_or_404(person_id) if person_id else None
    people = Person.query
    return render_template('person.html', title='人員列表', people=people, person=person)


@app.route('/get/meeting')
@login_required
def meeting_view():
    meeting_id = request.args.get('id')
    if not meeting_id:
        return abort(400)

    meeting = Meeting.query.get_or_404(int(meeting_id))

    # [Authority Restriction]
    # forbidden unauthorized user get in
    if not current_user.is_admin() and \
            current_user.id != meeting.chair_id and \
            current_user.id != meeting.minute_taker_id and \
            current_user not in meeting.attendees:
        return abort(403)
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
    return render_template('create.html', title='新增會議', people=people)


@app.route('/api/meeting/<int:meeting_id>')
@login_required
def meeting_api(meeting_id):
    meeting = Meeting.query.get_or_404(int(meeting_id))

    attendee = []
    guest = []
    att_present = []
    gue_present = []
    motions = []
    files = []

    for att in meeting.attendee_association:
        if att.is_member:
            attendee.append(att.person_id)
            if att.is_present:
                att_present.append(att.person_id)
        else:
            guest.append(att.person_id)
            if att.is_present:
                gue_present.append(att.person_id)

    for mot in meeting.motions:
        motion = {'description': mot.description,
                  'content': mot.content,
                  'status': mot.status.name,
                  'resolution': mot.resolution,
                  'execution': mot.execution}
        motions.append(motion)

    for file in meeting.attachments:
        filename = file.filename.split('-', 1)[1]
        filetype = filename.split('.')[-1]
        filetype = 'others' if filetype not in ['jpg', 'jpeg', 'png', 'pdf', 'txt', 'ppt', 'pptx', 'xls', 'xlsx', 'doc',
                                                'docx'] else filetype
        files.append({'file_id': file.id,
                      'file_name': filename[:-len(filetype) - 1],
                      'file_type': filetype})

    meet_info = {'title': meeting.title,
                 'time': int(mktime((meeting.time + timedelta(hours=8)).timetuple())) * 1000,
                 'location': meeting.location,
                 'type': meeting.type.name,
                 'chair': meeting.chair_id,
                 'minuteTaker': meeting.minute_taker_id,
                 'attendee': attendee,
                 'guest': guest,
                 'is_present': att_present + gue_present,
                 'chair_speech': meeting.chair_speech,
                 'announcements': [ann.content for ann in meeting.announcements],
                 'motions': motions,
                 'extempore': [ext.content for ext in meeting.extempores],
                 'files': files}

    return jsonify(meet_info)


@app.route('/new/meeting', methods=['POST'])
@login_required
def new_meeting():
    form = request.form
    data = json.loads(form['json_form'])
    files = request.files.getlist('files[]')

    print(data)

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
        # noinspection PyUnresolvedReferences
        return jsonify({'message': 'Success',
                        'person': {'id': person.id, 'name': person.name,
                                   'email': person.email, 'type': person.type.value}})


@app.route('/edit/meeting/<int:meeting_id>', methods=['GET', 'POST'])
@login_required
def edit_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(int(meeting_id))

    # [Authority Restriction]
    if not current_user.is_admin() and current_user.id != meeting.minute_taker_id:
        return abort(403)

    people = Person.query.all()

    if request.method == 'POST':
        form = request.form
        data = json.loads(form['json_form'])
        files = request.files.getlist('files[]')

        print(data)
        meeting.title = data['title']
        meeting.time = data['time']
        meeting.location = data['location']
        meeting.type = data['type']
        meeting.chair_id = int(data['chair'])
        meeting.minute_taker_id = int(data['minuteTaker'])
        meeting.chair_speech = data['chairSpeech']

        meeting.attendees.clear()
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

        meeting.announcements.clear()
        for content in data['announcement']:
            announcement = Announcement(content)
            meeting.announcements.append(announcement)

        meeting.motions.clear()
        for motion_form in data['motion']:
            motion = Motion(motion_form['MotionDescription'],
                            motion_form['MotionContent'],
                            motion_form['MotionStatus'],
                            motion_form['MotionResolution'],
                            motion_form['MotionExecution'])
            meeting.motions.append(motion)

        meeting.extempores.clear()
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

        db.session.commit()

        return jsonify({'message': 'Success'})
        # return redirect(url_for('meeting_page'))

    return render_template('edit-meeting.html', title=meeting.title, people=people)


@app.route('/edit/person/<int:person_id>', methods=['GET', 'POST'])
@login_required
def edit_person(person_id):
    # [Authority Restriction]
    if not current_user.is_admin():
        return abort(403)

    person = Person.query.get_or_404(int(person_id))
    if request.method == 'POST':
        form = request.form.to_dict()
        person.name = form['pNameInput']
        person.gender = form['pGenderInput']
        person.phone = form['pPhoneInput']
        person.email = form['pEmailInput']

        if person.type == 'Expert':
            person.expert_info = None
        elif person.type == 'Assistant':
            person.assistant_info = None
        elif person.type == 'DeptProf':
            person.dept_prof_info = None
        elif person.type == 'OtherProf':
            person.other_prof_info = None
        elif person.type == 'Student':
            person.student_info = None

        person.type = form['pTypeInput']

        if person.type == 'DeptProf':
            person.add_dept_prof_info(
                job_title=form['pJobTitleInput'],
                office_tel=form['pOfficeTelInput']
            )
        elif person.type == 'Assistant':
            person.add_assistant_info(
                office_tel=form['pOfficeTelInput']
            )
        elif person.type == 'OtherProf':
            person.add_other_prof_info(
                univ_name=form['pUnivNameInput'],
                dept_name=form['pDeptNameInput'],
                job_title=form['pJobTitleInput'],
                office_tel=form['pOfficeTelInput'],
                address=form['pAddressInput'],
                bank_account=form['pBankAccountInput']
            )
        elif person.type == 'Expert':
            person.add_expert_info(
                company_name=form['pCompanyNameInput'],
                job_title=form['pJobTitleInput'],
                office_tel=form['pOfficeTelInput'],
                address=form['pAddressInput'],
                bank_account=form['pBankAccountInput']
            )
        elif person.type == 'Student':
            if Student.query.filter_by(student_id=form['studentId']).first():
                return jsonify({'message': 'Student ID already exists'})
            person.add_student_info(
                student_id=form['pStudentIdInput'],
                program=form['pProgramInput'],
                study_year=form['pStudyYearInput']
            )
        db.session.commit()
        return redirect(url_for('person_page', person_id=person.id))
    return render_template('edit-person.html', title=person.name, person=person)


@app.route('/delete/meeting/<int:meeting_id>')
@login_required
def delete_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(int(meeting_id))
    # [Authority Restriction]
    if not current_user.is_admin() and current_user.id != meeting.minute_taker_id:
        return abort(403)

    for file in meeting.attachments:
        try:
            remove(file.file_path)
        except FileNotFoundError:
            print('FileNotFoundError: The system cannot find the path specified')
            abort(500)
    db.session.delete(meeting)
    db.session.commit()
    return redirect(url_for('meeting_page'))


@app.route('/delete/person/<int:person_id>')
@login_required
def delete_person(person_id):
    # [Authority Restriction]
    if not current_user.is_admin():
        return abort(403)
    person = Person.query.get_or_404(int(person_id))
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('person_page'))


@app.route('/uploads/<int:file_id>')
@login_required
def download(file_id):
    file = Attachment.query.filter_by(id=file_id).first()
    return send_file(path_or_file=file.file_path, as_attachment=False,
                     download_name=file.filename.split('-', 1)[1])


@app.route('/delete-file/<int:file_id>', methods=['POST'])
@login_required
def delete(file_id):
    file = Attachment.query.filter_by(id=file_id).first_or_404()
    try:
        remove(file.file_path)
    except FileNotFoundError:
        print('FileNotFoundError: The system cannot find the path specified')
        abort(500)
    db.session.delete(file)
    db.session.commit()
    return jsonify({'message': 'Success'})


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


def send_async_email(current_app, msg):
    with current_app.app_context():
        mail.send(msg)


@app.route('/mail/notice/<int:meeting_id>')
def send_meeting_notice(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    attendees = Attendee.query.filter_by(meeting_id=meeting_id)
    sender = ('會議管理系統', '110.database.csie.nuk@gmail.com')
    recipients = [att.email for att in meeting.attendees] + [meeting.chair.email]
    title = '開會通知 - ' + meeting.title
    msg = Message(title, sender=sender, recipients=recipients)
    msg.html = render_template('components/mail-meeting-minute.html', meeting=meeting, attendees=attendees, agenda=True)
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return 'Success', 200


@app.route('/mail/minute/<int:meeting_id>')
def send_meeting_minute(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    attendees = Attendee.query.filter_by(meeting_id=meeting_id)
    sender = ('會議管理系統', '110.database.csie.nuk@gmail.com')
    recipients = [att.email for att in meeting.attendees] + [meeting.chair.email]
    title = '會議結果 - ' + meeting.title
    msg = Message(title, sender=sender, recipients=recipients)
    msg.html = render_template('components/mail-meeting-minute.html', meeting=meeting, attendees=attendees)
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return 'Success', 200


@app.route('/mail/modify/<int:meeting_id>')
def send_meeting_modify_request(meeting_id):
    modify_request = request.args.get('modify')
    print(modify_request)

    meeting = Meeting.query.get_or_404(meeting_id)
    title = '請求修改會議紀錄 - ' + meeting.title
    sender = ('會議管理系統', '110.database.csie.nuk@gmail.com')
    recipients = [meeting.minute_taker.email]
    html = f'<h1>請求修改會議紀錄</h1><p>會議：{meeting.title}</p><p>來自：{current_user.name}</p><p>{modify_request}</p>'
    msg = Message(title, sender=sender, recipients=recipients)
    msg.html = html
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return 'Success', 200


@app.route('/confirm')
def confirm_check():
    person_id = request.args.get('person_id')
    meeting_id = request.args.get('meeting_id')
    meeting = Meeting.query.get(meeting_id)

    if request.args.get('confirm') == 'true':
        if str(meeting.chair_id) == person_id:
            meeting.chair_confirmed = True
        else:
            attendee = Attendee.query.filter_by(person_id=person_id, meeting_id=meeting_id).first()
            attendee.is_confirmed = True
    else:
        if str(meeting.chair_id) == person_id:
            meeting.chair_confirmed = False
        else:
            attendee = Attendee.query.filter_by(person_id=person_id, meeting_id=meeting_id).first()
            attendee.is_confirmed = False

    db.session.commit()
    return 'Success', 200
