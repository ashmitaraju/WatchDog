from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField,  TextField, ValidationError , IntegerField
from wtforms.validators import DataRequired, InputRequired, Email, EqualTo, Required , Optional, StopValidation
from wtforms.fields.html5 import DateField

from .models import *

from flask_wtf.file import FileField, FileAllowed, FileRequired

from app import images

def myvalidator(form, field):

    if not form.image.data:

        field.errors[:] = []
        raise StopValidation()

class LoginForm(Form):
    email = StringField('E-mail', validators =[DataRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    submit = SubmitField('Login')

class SignUpForm(Form):
    email = StringField('E-Mail', validators = [InputRequired(), Email()])
    username = StringField('Username', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use')

    def validate_username(self, field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use')

class EditProfileForm(Form):
    first_name = TextField('First Name', validators = [InputRequired()])
    last_name = TextField('Last Name', validators = [Optional()])
    submit = SubmitField('Save')

class EditImageGalleryForm(Form):

    name = StringField('Add New Person', validators = [InputRequired()])
    image = FileField('Upload Picture(s)', validators=[myvalidator, Optional() , FileAllowed(images, 'Image only!')])
    picture = SubmitField('Take Pictures')
    submit = SubmitField('Add Images')
    skip = SubmitField('Submit and Train')

