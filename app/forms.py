from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import SubmitField, StringField, PasswordField, validators, IntegerField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Length


class ImageForm(FlaskForm):
    picture = FileField('Upload image', validators=[
                        FileAllowed(['jpg', 'png', 'jpeg']), InputRequired()])
    submit = SubmitField('Submit')


class DetailsForm(FlaskForm):
    age = IntegerField('Age', [validators.DataRequired()])
    height = IntegerField('Height', [validators.DataRequired()])
    weight = IntegerField('Weight', [validators.DataRequired()])
    bloodgrp = StringField('Blood-grp', [validators.DataRequired()])
    submit = SubmitField('Submit')


class AddMemberForm(FlaskForm):
    new_email = StringField('Email address', [validators.DataRequired(),
                                              validators.Email()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField('Email address', [validators.DataRequired(),
                                          validators.Email()])
    password = PasswordField('Password', [
        validators.DataRequired(),
    ])
    submit = SubmitField('Submit')


class SignupForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    mobile = StringField('Mobile', validators=[
                         DataRequired(), Length(min=10, max=10)])
    email = StringField('Email address', [validators.DataRequired(),
                                          validators.Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
