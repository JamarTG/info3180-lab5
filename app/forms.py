# Add any form classes for Flask-WTF here
from wtforms import Form
from wtforms import StringField,TextAreaField, FileField, validators

class MovieForm(Form):
    title = StringField('Title',[validators.InputRequired(),validators.Length(max=50)])
    description = TextAreaField('Description',[validators.InputRequired(),validators.Length(max=0)])
    poster = FileField('Poster', [validators.InputRequired()])
