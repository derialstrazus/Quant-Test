from flask.ext.wtf import Form
from wtforms import StringField, TextField, BooleanField
from wtforms.validators import DataRequired


class SecurityForm(Form):
    security = StringField('security', validators=[DataRequired()])