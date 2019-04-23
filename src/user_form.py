from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_user import login_required, UserManager, UserMixin, current_user


# Todo set default values fetched from user table
class Form(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    height = StringField('height', validators=[DataRequired()])
    age = StringField('age', validators=[DataRequired()])
    gender = StringField('gender', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
