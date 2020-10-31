from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import SubmitField, StringField, PasswordField, validators
from wtforms.validators import InputRequired, DataRequired, EqualTo


class ImageForm(FlaskForm):
    picture = FileField('Upload image', validators=[
                        FileAllowed(['jpg', 'png', 'jpeg']), InputRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField('Email address', [validators.DataRequired(),
                                          validators.Email()])
    password = PasswordField('Password', [
        validators.DataRequired(),
    ])
    submit = SubmitField('Submit')
