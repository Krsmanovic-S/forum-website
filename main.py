from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from database_classes import *
from forms import *
from datetime import datetime


# App Initialization and other modules
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SESSION_PERMANENT'] = False
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(app)
bootstrap = Bootstrap5(app)


# Database - classes are in database_classes.py
db.init_app(app)
with app.app_context():
    db.create_all()


# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/', methods=["GET"])
def home():
    return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if request.method == "POST" and register_form.validate_on_submit():
        entered_username = request.form.get('username')
        entered_email = request.form.get('email')
        # Check for an existing username
        existing_username = db.session.execute(db.select(User).where(User.username == entered_username)).scalar()
        if existing_username:
            flash("Username already exists.")
            return redirect(url_for('register', form=register_form))
        # Check for existing email
        existing_email = db.session.execute(db.select(User).where(User.email == entered_email)).scalar()
        if existing_email:
            flash("Email already exists.")
            return redirect(url_for('register', form=register_form))
        # Check if passwords match
        entered_password = request.form.get('password')
        if entered_password != request.form.get('repeat_password'):
            flash("Passwords do not match.")
            return redirect(url_for('register', form=register_form))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            username=entered_username,
            email=entered_email,
            password=hash_and_salted_password
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('register.html', form=register_form)


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if request.method == "POST":
        user = db.session.execute(db.select(User).where(User.username == request.form.get('username'))).scalar()
        # Check for wrong username
        if not user:
            flash("Username does not exist, please try again.")
            return redirect(url_for('login', form=login_form))
        # Check the password
        elif not check_password_hash(user.password, request.form.get('password')):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login', form=login_form))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html", form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/create-post", methods=["GET", "POST"])
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = ForumPost(
            title=form.title.data,
            body=form.body.data,
            author=current_user,
            date=datetime.today().strftime("%B %d, %Y"),
            category=request.form.get('category')
        )

        #db.session.add(new_post)
        #db.session.commit()
        return redirect(url_for('home'))
    return render_template('create-post.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)