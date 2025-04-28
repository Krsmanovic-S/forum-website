from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, URL, Email, Regexp, EqualTo
from flask_ckeditor import CKEditorField
from database_classes import ForumCategories


class RegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[
        DataRequired(),
        Regexp(r'^[A-Za-z0-9]+$', message="Username must contain only letters and numbers.")
    ])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    repeat_password = PasswordField(label="Repeat Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[
        DataRequired(),
        Regexp(r'^[A-Za-z0-9]+$', message="Username must contain only letters and numbers.")
    ])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class CreatePostForm(FlaskForm):
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    title = StringField("Post Title", validators=[DataRequired()])
    body = CKEditorField("Post Content", validators=[DataRequired()])
    submit = SubmitField("Create Post")

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        categories = ForumCategories.query.all()
        self.category.choices = [(category.id, category.name) for category in categories]