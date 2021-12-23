from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user

from main import app
from main.models import Person


@app.route('/')
def home():
    return render_template('meeting.html')


@app.route('/new')
def create():
    return render_template('create.html')


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
