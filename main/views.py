import json
from datetime import timedelta
from functools import wraps
from os import path, remove
from threading import Thread
from time import mktime

from flask import render_template, redirect, url_for, flash, request, jsonify, send_file, abort
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from sqlalchemy import desc, or_
from sqlalchemy.exc import DataError

from main import app, mail
from main.models import Person, db, Student, Attachment, Meeting, Announcement, Motion, Extempore, Attendee, Feedback


def admin_required(func):
    """
    限管理員使用路由裝飾器
    :param func: 路由函式
    :type func: function
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin():
            abort(403)
        return func(*args, **kwargs)

    return decorated_view


@app.route('/')
@login_required
def home():
    return redirect(url_for('meeting_page'))


@app.route('/new')
@login_required
@admin_required
def create_meeting_minute_page():
    """
    顯示新增會議頁面
    :return: 新增會議頁面
    """
    people = Person.query.all()
    return render_template('meeting-new.html', title='新增會議', people=people)


@app.route('/meeting')
@app.route('/meeting/<int:meeting_id>')
@login_required
def meeting_page(meeting_id=None):
    """
    顯示會議記錄列表
    :param meeting_id: 會議編號
    :return: 會議紀律列表
    """
    meetings = Meeting.query.filter(or_(
        Meeting.chair.has(id=current_user.id),
        Meeting.minute_taker.has(id=current_user.id),
        Meeting.attendees.any(id=current_user.id)
    )).order_by(desc(Meeting.time))

    if current_user.is_admin():
        meetings = Meeting.query.order_by(desc(Meeting.time))

    meeting = Meeting.query.get_or_404(meeting_id) if meeting_id else None
    attendees = Attendee.query.filter_by(meeting_id=meeting_id)
    return render_template('meeting.html', title='會議列表', meetings=meetings,
                           meeting=meeting, attendees=attendees, timedelta=timedelta)


@app.route('/calendar')
@login_required
def calendar_page():
    """
    顯示會議行事曆頁面
    :return: 會議行事曆頁面
    """
    meetings = Meeting.query.filter(or_(
        Meeting.chair.has(id=current_user.id),
        Meeting.minute_taker.has(id=current_user.id),
        Meeting.attendees.any(id=current_user.id)
    ))

    if current_user.is_admin():
        meetings = Meeting.query

    return render_template('calendar.html', title='會議行事曆', meetings=meetings)


@app.route('/motion')
@login_required
def motion_page():
    """
    顯示討論事項（決策追蹤）列表頁面
    :return: 討論事項列表頁面
    """
    meetings = Meeting.query.filter(or_(
        Meeting.chair.has(id=current_user.id),
        Meeting.minute_taker.has(id=current_user.id),
        Meeting.attendees.any(id=current_user.id)
    ))
    motions = Motion.query.join(meetings.subquery()).join(Meeting).order_by(Motion.status, Meeting.time)

    if current_user.is_admin():
        motions = Motion.query.join(Meeting).order_by(Motion.status, Meeting.time)

    return render_template('motion.html', title='決策追蹤', motions=motions)


@app.route('/person')
@app.route('/person/<int:person_id>')
@login_required
def person_page(person_id=None):
    """
    顯示人員列表頁面
    :param person_id: 人員編號
    :return: 人員列表頁面
    """
    people = Person.query.order_by(Person.name)
    person = people.get_or_404(person_id) if person_id else None
    return render_template('person.html', title='人員列表', people=people, person=person)


@app.route('/statistics')
@login_required
@admin_required
def statistics_page():
    """
    顯示統計資料頁面
    :return: 統計資料頁面
    """
    return render_template('statistics.html', title='統計資料')


@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback_page():
    """
    顯示學生匿名意見
    :return: 學生意見頁面
    """
    if request.method == 'POST':
        feedback = Feedback(content=request.form['feedbackText'])
        db.session.add(feedback)
        db.session.commit()
        return redirect(url_for('feedback_page'))
    feedback = Feedback.query.order_by(desc(Feedback.id)).all()
    return render_template('feedback.html', title='學生意見', feedback=feedback, timedelta=timedelta)


@app.route('/get/meeting')
@login_required
def meeting_view():
    """
    顯示會議記錄區塊，利用 JavaScript 呼叫並更新前端
    :request.args id: 會議編號
    :return: 會議記錄區塊
    """
    meeting_id = request.args.get('id')
    if not meeting_id:
        return abort(400)
    meeting = Meeting.query.get_or_404(int(meeting_id))
    attendees = Attendee.query.filter_by(meeting_id=meeting_id)
    return render_template('components/meeting-view.html', meeting=meeting, attendees=attendees)


@app.route('/get/motion')
@login_required
def motion_view():
    """
    顯示討論事項（決策追蹤）區塊，利用 JavaScript 呼叫並更新前端
    :request.args id: 討論事項編號
    :return: 討論事項區塊
    """
    motion_id = request.args.get('id')
    if not motion_id:
        return abort(400)
    motion = Motion.query.filter_by(id=motion_id).first_or_404(int(motion_id))
    return render_template('components/motion-view.html', motion=motion)


@app.route('/get/person')
@login_required
def person_view():
    """
    顯示人員資訊區塊，利用 JavaScript 呼叫並更新前端
    :request.args id: 人員編號
    :return: 人員資訊區塊
    """
    person_id = request.args.get('id')
    if not person_id:
        return abort(404)
    person = Person.query.get_or_404(int(person_id))
    return render_template('components/person-view.html', person=person)


@app.route('/new/meeting', methods=['POST'])
@login_required
@admin_required
def new_meeting():
    """
    新增會議記錄 API
    :request.form json_form: 新增會議表單
    :request.files files[]: 附件檔案
    :return: JSON 物件
    """
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

    db.session.add(meeting)
    db.session.commit()

    attendees = meeting.attendee_association
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

    db.session.commit()
    return jsonify({'message': 'Success'})


@app.route('/new/person', methods=['POST'])
@login_required
@admin_required
def new_person():
    """
    新增人員 API
    :request.form: 新增人員表單
    :return: JSON 物件
    """
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
@admin_required
def edit_meeting(meeting_id):
    """
    編輯會議紀錄
    :request.form json_form: 編輯會議表單
    :request.files files[]: 附件檔案
    :param meeting_id: 會議編號
    :return: 編輯會議紀錄頁面
    """
    meeting = Meeting.query.get_or_404(int(meeting_id))
    people = Person.query.all()

    if request.method == 'POST':
        form = request.form
        data = json.loads(form['json_form'])
        files = request.files.getlist('files[]')

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
    return render_template('meeting-edit.html', title=meeting.title, people=people)


@app.route('/edit/person/<int:person_id>', methods=['GET', 'POST'])
@login_required
def edit_person(person_id):
    """
    編輯人員資訊
    :param person_id: 人員編號
    :return: 編輯人員資訊頁面
    """
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
            person.add_student_info(
                student_id=form['pStudentIdInput'],
                program=form['pProgramInput'],
                study_year=form['pStudyYearInput']
            )
        db.session.commit()
        return redirect(url_for('person_page', person_id=person.id))
    return render_template('person-edit.html', title=person.name, person=person)


@app.route('/delete/meeting/<int:meeting_id>')
@login_required
@admin_required
def delete_meeting(meeting_id):
    """
    刪除會議記錄
    :param meeting_id: 會議編號
    :return: 重新導向至會議列表頁面
    """
    meeting = Meeting.query.get_or_404(int(meeting_id))
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
@admin_required
def delete_person(person_id):
    """
    刪除人員
    :param person_id: 人員編號
    :return: 重新導向至人員列表頁面
    """
    person = Person.query.get_or_404(int(person_id))
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('person_page'))


@app.route('/delete/attachment/<int:file_id>', methods=['POST'])
@login_required
@admin_required
def delete_attachment(file_id):
    """
    刪除附件檔案
    :param file_id: 檔案編號
    :return: JSON 物件
    """
    file = Attachment.query.filter_by(id=file_id).first_or_404()
    try:
        remove(file.file_path)
    except FileNotFoundError:
        print('FileNotFoundError: The system cannot find the path specified')
        abort(500)
    db.session.delete(file)
    db.session.commit()
    return jsonify({'message': 'Success'})


@app.route('/uploads/<int:file_id>')
@login_required
@admin_required
def download_attachment(file_id):
    """
    下載附件檔案
    :param file_id: 檔案編號
    :return: 檔案
    """
    file = Attachment.query.filter_by(id=file_id).first()
    return send_file(path_or_file=file.file_path, as_attachment=False,
                     download_name=file.filename.split('-', 1)[1])


@app.route('/api/meeting/<int:meeting_id>')
@login_required
@admin_required
def meeting_api(meeting_id):
    """
    會議記錄 API
    :param meeting_id: 會議編號
    :return: JSON 物件
    """
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    登入使用者
    :request.form email: 電子郵件
    :return: 登入頁面
    """
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
    """
    登出使用者
    :return: 重新導向至登入頁面
    """
    logout_user()
    return redirect(url_for('login'))


def send_async_email(current_app, msg):
    """
    送出電子郵件 (用於異步處理)
    :param current_app: Flask 實例
    :param msg: flask_mail.Message 物件
    """
    with current_app.app_context():
        mail.send(msg)


@app.route('/mail/notice/<int:meeting_id>')
@login_required
@admin_required
def send_meeting_notice(meeting_id):
    """
    以電子郵件寄送會議通知
    :param meeting_id: 會議編號
    :return: HTTP Response 200
    """
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
@login_required
@admin_required
def send_meeting_minute(meeting_id):
    """
    以電子郵件寄送會議紀錄
    :param meeting_id: 會議編號
    :return: HTTP Response 200
    """
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
@login_required
def send_meeting_modify_request(meeting_id):
    """
    以電子郵件寄送會議修改請求
    :request.args modify: 訊息內容
    :param meeting_id: 會議編號
    :return: HTTP Response 200
    """
    modify_request = request.args.get('modify')
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
@login_required
def confirm_meeting_minute():
    """
    與會人員確認會議
    :request.args person_id: 人員編號
    :request.args meeting_id: 會議編號
    :request.args confirm: 確認 或 取消確認
    :return: HTTP Response 200
    """
    person_id = request.args.get('person_id')
    meeting_id = request.args.get('meeting_id')
    meeting = Meeting.query.get(meeting_id)

    if request.args.get('confirm') == 'true':
        if str(meeting.chair_id) == person_id:
            meeting.chair_confirmed = True
        else:
            attendee = Attendee.query.filter_by(person_id=person_id, meeting_id=meeting_id).first()
            attendee.is_confirmed = True

        all_confirmed = meeting.chair_confirmed
        for attendee in meeting.attendees:
            a = Attendee.query.filter_by(person_id=attendee.id, meeting_id=meeting.id).first()
            all_confirmed = all_confirmed and a.is_confirmed
        if all_confirmed:
            meeting.archived = True
            db.session.commit()
            return 'Archived', 200
    else:
        if str(meeting.chair_id) == person_id:
            meeting.chair_confirmed = False
        else:
            attendee = Attendee.query.filter_by(person_id=person_id, meeting_id=meeting_id).first()
            attendee.is_confirmed = False

    db.session.commit()
    return 'Success', 200
