from flask import Flask, render_template, flash, request, redirect, url_for, session, abort
# from flask_security import Security, SQLAlchemyUserDatastore,UserMixin, RoleMixin, login_required
from flask_login import LoginManager, login_user, logout_user, UserMixin, current_user
from flask_sqlalchemy import SQLAlchemy
from .forms.forms import RegistrationForm, LoginForm, BusinessForm, BusinessCategoryForm
# from models.models import User
from flask.views import View
import sys
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
# app.config['SECRET_REGISTERABLE'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jamohsize@localhost/jamii_business'
db = SQLAlchemy(app)
login = LoginManager()
login.init_app(app)
login.login_view = 'login'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    business = db.relationship('Business', backref='owner', lazy=True)
    is_active = db.Column(db.Boolean())

    def __repr__(self):
        return f"User('{self.username}, {self.email}, {self.image_file}')"

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Businesscategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.name}')"


class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    category = db.Column(db.Integer, db.ForeignKey(
        'businesscategory.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(20), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Business('{self.name}, {self.owner}, {self.location}')"


@app.route('/')
@app.route('/home')
def home():
    context = {
        'title': "Welcome",
    }
    return render_template("home.html", context=context)


@app.route('/register', methods=['GET', 'POST'])
def register():
    users = {}
    form = RegistrationForm()
    context = {
        'form': form,
    }

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username=username, email=email,
                    password=password, is_active=True)
        db.session.add(user)
        db.session.commit()

        flash(f'Account Created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template("register.html", context=context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    context = {
        'form': form,
    }
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user is not None:
            user_email = user.email
            user_password = user.password

            if password == user_password:
                flash(f'Successfully for Logged In!', 'success')
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash(f'Username or Password does not match!', 'danger')
        else:
            flash(f'User Does Not exist!', 'danger')

    return render_template("login.html", context=context)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash(f'Successfully Logged Out!', 'success')
    return redirect(url_for('home'))

# Register a business


@app.route('/businesses', methods=['GET', 'POST'])
def businesses():
    form = BusinessForm()
    category_form = BusinessCategoryForm()

    business_category = Businesscategory.query.all()

    context = {
        'form': form,
        'category_form':category_form
    }

    if form.validate_on_submit():
        name = form.business_name.data
        category = form.business_category.data
        description = form.business_description.data
        location = form.business_location.data

        business = Business(name=name, category=1,description=description, location=location, user_id=current_user.id,rating=0)
        db.session.add(business)
        db.session.commit()

        flash(f'Business successfully Created!', 'success')
        return redirect(url_for('getBusiness'))

    return render_template("create.html", context=context)

@app.route('/category', methods=['POST'])
def category():
    category_form = BusinessCategoryForm()

    if category_form.validate_on_submit():
        name = category_form.category_name.data

        business_category = Businesscategory(name=name)
        db.session.add(business_category)
        db.session.commit()

        flash(f'Business Category successfully Created!', 'success')
        return redirect(url_for('businesses'))

    return redirect(url_for('businesses'))


# Update business profile
# @app.route('/businesses/<businessId>', methods=['GET', 'POST'])
# def updateBusiness():
#     flash(f'Successfully Updated Info!', 'success')
#     return redirect(url_for('login'))

# # Remove a business
# @app.route('/businesses/<businessId>', methods=['GET', 'POST'])
# def deleteBusiness():
#     flash(f'Successfully Deleted!', 'success')
#     return redirect(url_for('login'))
#
# get a business


@app.route('/business', methods=['GET', 'POST'])
def getBusiness():
    businesses = Business.query.all()

    context = {
        'businesses': businesses,
    }

    return render_template('business.html', context=context)


@app.route('/businesses/<string:id>/', methods=['GET', 'POST'])
def BusinessDetail(id):
    business = Business.query.filter_by(id=id).first()
    context = {
        'business': business,
    }

    return render_template('business_details.html', context=context)

def addNumber(no_1,no_2):
    add = no_1+no_2
    return add



if __name__ == '__main__':
    app.run(debug=True)
