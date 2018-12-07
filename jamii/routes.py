from flask import render_template, flash, request, redirect, url_for, session, abort
from flask_login import  login_user, logout_user, current_user, login_required
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
from jamii.forms.forms import RegistrationForm, LoginForm, BusinessForm, BusinessCategoryForm, UpdateAccountForm, UpdateBusinessForm
from jamii import app, db, bcrypt
from jamii.models.models import User, Business, Businesscategory, BusinessReviews
import secrets
import os



@app.route('/')
@app.route('/home')
def home():
    context = {
        'title': "Welcome",
    }
    return render_template("home.html", context=context)


@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    context = {
        'form': form,
    }

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email,
                    password=pw_hash)

        db.session.add(user)
        db.session.commit()

        flash(f'Account Created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template("register.html", context=context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    context = {
        'form': form,
    }
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(email=email).first()
        if user:
            user_email = user.email
            pw_hash = user.password
            user_password = bcrypt.check_password_hash(pw_hash, password)

            if user_password:
                flash(f'Successfully Logged In!', 'success')
                login_user(user,remember=remember)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
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
@login_required
def businesses():
    form = BusinessForm()
    category_form = BusinessCategoryForm()

    business_category = Businesscategory.query.all()

    context = {
        'form': form,
        'category_form':category_form,
        'businesses':14

    }

    if form.validate_on_submit():
        name = form.business_name.data
        category = form.business_category.data
        description = form.business_description.data
        location = form.business_location.data

        business = Business(name=name, category=1,description=description, location=location, user_id=current_user.id, rating=0)
        db.session.add(business)
        db.session.commit()

        flash(f'Business successfully Created!', 'success')
        return redirect(url_for('getBusiness'))

    return render_template("create.html", context=context)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/media/images/profile_pic', picture_fn)
    output_size = (150,150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    account_form = UpdateAccountForm()
    business_category = Businesscategory.query.all()
    businesses = Business.query.filter_by(owner=current_user)

    context = {
        'account_form':account_form,
        'business_no':14,
        'businesses':businesses

    }
    if account_form.validate_on_submit():
        if account_form.profile.data:
            picture_file = save_picture(account_form.profile.data)
            current_user.image_file = picture_file

        username = account_form.username.data
        email = account_form.email.data

        current_user.username = username
        current_user.email = email
        db.session.commit()
        flash(f'Account Info successfully Updated!', 'success')
        return redirect(url_for('dashboard'))

    elif request.method == "GET":
        account_form.username.data = current_user.username
        account_form.email.data = current_user.email

    return render_template("dashboard.html", context=context)

@app.route('/category', methods=['POST'])
@login_required
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
@app.route('/businesses/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def updateBusiness(id):
    business = Business.query.get_or_404(id)
    business_form = UpdateBusinessForm()
    context = {
        'business': business,
        'business_form':business_form,
    }
    if business.owner != current_user:
        abort(403)

    if business_form.validate_on_submit():
        name = business_form.business_name.data
        # category = business_form.business_category.data
        description = business_form.business_description.data
        location = business_form.business_location.data

        business.name=name
        business.category=1
        business.description=description
        business.location=location
        db.session.commit()
        flash(f'Successfully Updated Business !', 'success')
        return redirect(url_for('getBusiness'))
    elif request.method == "GET":
        business_form.business_name.data = business.name
        business_form.business_category.data = business.category
        business_form.business_description.data = business.description
        business_form.business_location.data = business.location



    return render_template('edit_business.html', context=context)

# Remove a business
@app.route('/businesses/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteBusiness(id):
    business = Business.query.get_or_404(id)
    if business.owner != current_user:
        abort(403)
    flash(f'Successfully Deleted!', 'success')
    return redirect(url_for('login'))

# get a business
@app.route('/business', methods=['GET', 'POST'])
def getBusiness():
    businesses = Business.query.all()

    context = {
        'businesses': businesses,
    }

    return render_template('business.html', context=context)


@app.route('/businesses/<int:id>/', methods=['GET', 'POST'])
def BusinessDetail(id):
    business = Business.query.get_or_404(id)
    context = {
        'business': business,
    }

    return render_template('business_details.html', context=context)