from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    """Class for a login form"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Admin Login')


class CreatePostForm(FlaskForm):
    """Class for different posts for projects"""
    title = StringField("Project title", validators=[DataRequired()])
    category = SelectField('Category', choices=[('ml', 'Machine Learning'), ('web', 'Web'), ('games', 'Games')],
                           validators=[DataRequired()])
    project_url = StringField("Project URL", validators=[URL()])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField("Submit Post")
