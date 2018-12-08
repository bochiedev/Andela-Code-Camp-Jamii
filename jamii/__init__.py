import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_humanize import Humanize





app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jamohsize@localhost/jamii_business'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['HUMANIZE_USE_UTC'] = True
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt(app)
humanize = Humanize(app)


from jamii import routes

@humanize.localeselector
def get_locale():
    return 'EAT'
