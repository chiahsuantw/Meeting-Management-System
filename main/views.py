from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user
from sqlalchemy.exc import DataError
from werkzeug.exceptions import BadRequestKeyError

from main import app
from main.models import Person, db, Student


@app.route('/')
def home():
    return render_template('meeting.html')


@app.route('/new')
def create():
    people = Person.query.all()
    return render_template('create.html', people=people)


@app.route('/new/person', methods=['POST'])
def new_person():
    form = request.form
    print(form)

    if Person.query.filter_by(email=form['email']).first():
        return jsonify({'validate': 'Person already exists'})

    person = Person()
    person.name = form['name']
    person.gender = form['gender']
    person.phone = form['phone']
    person.email = form['email']
    person.type = form['type']

    if person.type == 'DeptProf':
        person.add_dept_prof(job_title=form['jobTitle'],
                             office_tel=form['officeTel'])
    elif person.type == 'Assistant':
        person.add_assistant(office_tel=form['officeTel'])
    elif person.type == 'OtherProf':
        person.add_other_prof(univ_name=form['univName'],
                              dept_name=form['deptName'],
                              job_title=form['jobTitle'],
                              office_tel=form['officeTel'],
                              address=form['address'],
                              bank_account=form['bankAccount'])
    elif person.type == 'Expert':
        person.add_expert(company_name=form['companyName'],
                          job_title=form['jobTitle'],
                          office_tel=form['officeTel'],
                          address=form['address'],
                          bank_account=form['bankAccount'])
    elif person.type == 'Student':
        if Student.query.filter_by(student_id=form['studentId']).first():
            return jsonify({'validate': 'Student ID already exists'})
        person.add_student(student_id=form['studentId'],
                           program=form['program'],
                           study_year=form['studyYear'])
    try:
        db.session.add(person)
        db.session.commit()
    except DataError:
        return jsonify({'validate': 'Error'})
    finally:
        return jsonify({'validate': 'Success'})


@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    if email:
        user = Person.query.filter_by(email=email).first()
        if user:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('登入資訊不正確，請再試一次', 'danger')

    return render_template('login.html', title='登入')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/person_api')
def person_api():
    person_dict = {}
    people = Person.query.all()
    for person in people:
        person_dict[person.id] = {"name": person.name, "type": person.type.value}

    return jsonify(person_dict)
