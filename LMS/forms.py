from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField,SelectField,BooleanField, IntegerField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from LMS.models import User,Faculty
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('LoginId',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That UserId is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    user_type = SelectField('User Type', choices=[('student', 'Student'), ('faculty', 'Faculty')])
    email = StringField('LoginId', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class FacultyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    designation = StringField('Designation', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    cabin = StringField('Cabin', validators=[DataRequired()])
    availability = StringField('Availability', validators=[DataRequired()])
    remark = StringField('Remark', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class UpdateAccountForm(FlaskForm):
    username = StringField('Name', 
                           validators=[DataRequired(),Length(min=2 , max=20)])
    email = StringField('LoginId',validators=[DataRequired()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png','jpeg'])])

    submit = SubmitField('Update')

        
    def validate_email(self, email):
        if email.data != current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That UserId is Taken! Please Choose a different one.')

class UpdateFacultyAccountForm(UpdateAccountForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    designation = StringField('Designation', validators=[DataRequired(), Length(min=2, max=20)])
    school = StringField('School', validators=[DataRequired(), Length(min=2, max=50)])
    cabin = StringField('Cabin', validators=[DataRequired(), Length(min=2, max=20)])

    def validate_name(self, name):
        if name.data != current_user.name:
            faculty = Faculty.query.filter_by(name=name.data).first()
            if faculty:
                raise ValidationError('That Name is Taken! Please Choose a different one.') 


