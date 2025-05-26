from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FileField, IntegerField, DateField, ValidationError
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Email, Regexp, NumberRange
from flask_ckeditor import CKEditorField
from database_classes import ForumCategories
from flask_wtf.file import FileAllowed


# For limiting profile image uploads to 1MB
def file_size_limit(max_size_mb):
    max_bytes = max_size_mb * 1024 * 1024

    def _file_size_limit(form, field):
        if field.data:
            field.data.stream.seek(0, 2)  # Seek to end
            file_size = field.data.stream.tell()
            field.data.stream.seek(0)  # Reset pointer to beginning

            if file_size > max_bytes:
                raise ValidationError(f'File size must be less than {max_size_mb}MB.')
    return _file_size_limit


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


class EditProfileForm(FlaskForm):
    image = FileField("Profile Image", validators=[
        FileAllowed(['png'], "Only .png files are allowed."),
        file_size_limit(1)])
    description = CKEditorField("Profile Description")
    date_of_birth = DateField(
        "Date of Birth",
        format='%Y-%m-%d',
        render_kw={"placeholder": "2025-01-01", "type": "date"}
    )
    years_training = IntegerField("How many years have you been training?", validators=[NumberRange(min=0, max=50)], default=0)
    gender = SelectField(
        "Select Gender",
        choices=[
            ("NOT_SPECIFIED", "Don't Specify"),
            ("MALE", "Male"),
            ("FEMALE", "Female"),
            ("OTHER", "Other")
        ]
    )

    submit = SubmitField("Save Changes")