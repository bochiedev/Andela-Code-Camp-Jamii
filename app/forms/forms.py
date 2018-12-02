from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class BusinessForm(FlaskForm):
    business_name = StringField('Business Name', validators=[DataRequired()])
    business_description = TextAreaField('Business Description', validators=[DataRequired()])
    business_location = StringField('Location', validators=[DataRequired()])
    business_category = SelectField(u'Category', choices=[('aim', 'AIM'), ('msn', 'MSN')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class BusinessCategoryForm(FlaskForm):
    category_name = StringField('Business Name', validators=[DataRequired()])
    submit = SubmitField('Create')
