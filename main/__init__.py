from os import path
from pathlib import Path

from flask import Flask
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/meeting_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'b4f576c819524c45fa389ced800edafb'
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = path.join(app.root_path, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

# Create upload folder if it doesn't exist
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

db = SQLAlchemy(app)
login = LoginManager(app)
moment = Moment(app)

from main import views, models
