from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from jamii.models.models import User, Businesscategory



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password'),Length(min=6, max=20)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken. Please choose a different username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken. Please choose a different email')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile = FileField('Update Profile Pic', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is taken. Please use a different username')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is taken. Please use a different email')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class BusinessForm(FlaskForm):

    def category_data():
        data = Businesscategory.query.all()
        return data

    business_name = StringField('Business Name', validators=[DataRequired()])
    business_description = TextAreaField('Business Description', validators=[DataRequired()])
    business_location = StringField('Location', validators=[DataRequired()])
    business_category = QuerySelectField(u'Skill level',
                               validators=[DataRequired()],
                               query_factory=category_data)
    # business_category = SelectField(u'Category', choices=list(category_data()), validators=[DataRequired()])
    submit = SubmitField('Create')

    # def category_data(self):
    #     data = BusinessCategory.query.all()
    #     business_category.choices = data
    #     return data

class UpdateBusinessForm(FlaskForm):

    def category_data():
        data = Businesscategory.query.all()
        return data

    business_name = StringField('Business Name', validators=[DataRequired()])
    business_description = TextAreaField('Business Description', validators=[DataRequired()])
    business_location = StringField('Location', validators=[DataRequired()])
    # business_category = SelectField(u'Category', choices=list(category_data()), validators=[DataRequired()])
    business_category = QuerySelectField(u'Skill level',
                               validators=[DataRequired()],
                               query_factory=category_data)
    submit = SubmitField('Update')



class BusinessCategoryForm(FlaskForm):
    category_name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Create')

class BusinessReviewForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    rating = IntegerField('Rating Score', validators=[DataRequired()])
    message = TextAreaField('Review Message', validators=[DataRequired()])
    submit = SubmitField('Create')

    def validate_rating(self, rating):

        if rating.data > 5:
            raise ValidationError('Rating Must Be between 1 and 5')
