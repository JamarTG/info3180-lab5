# Add any form classes for Flask-WTF here
from wtforms import Form
from wtforms import StringField,TextAreaField, FileField, validators
from flask_wtf.file import FileAllowed
from flask_wtf import FlaskForm


class MovieForm(FlaskForm):
    title = StringField('Title',[validators.InputRequired(),validators.Length(max=50)])
    description = TextAreaField('Description',[validators.InputRequired(),validators.Length(max=200)])
    poster = FileField('Poster', [validators.InputRequired(),FileAllowed(['jpg', 'png'], 'Images only!'),])
