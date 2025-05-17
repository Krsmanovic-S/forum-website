from flask import Flask, render_template, redirect, url_for, request, flash
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from database_classes import *
from forms import *
from datetime import datetime
from sqlalchemy import func
from post_search import es, index_post, search_posts


# App Initialization and other modules
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SESSION_PERMANENT'] = False
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(app)
bootstrap = Bootstrap5(app)
CURRENT_POLL_ID = 1

# Database Initialization - all db classes are in database_classes.py
db.init_app(app)
with app.app_context():
    db.create_all()
migrate = Migrate(app, db)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/', methods=["GET"])
def home():
    category_name = request.args.get("category", type=str)
    search_query = request.args.get('search')
    if category_name:
        category_name.replace('+', '')
        posts = (
            db.session.query(ForumPost)
            .join(ForumCategories)
            .filter(ForumCategories.name == category_name)
            .order_by(ForumPost.date.desc())
            .all()
        )
    elif search_query:
        posts = search_posts(search_query)
    else:
        posts = ForumPost.query.order_by(ForumPost.date.desc()).all()

    categories = ForumCategories.query.all()
    votes_by_post = {}
    if current_user.is_authenticated:
        user_votes = PostVote.query.filter_by(user_id=current_user.id).all()
        for vote in user_votes:
            votes_by_post[vote.post_id] = vote.value

    trending_posts = (
        db.session.query(ForumPost, func.coalesce(func.sum(PostVote.value), 0).label("score"))
        .outerjoin(PostVote, ForumPost.id == PostVote.post_id)
        .group_by(ForumPost.id)
        .order_by(func.coalesce(func.sum(PostVote.value), 0).desc())
        .limit(3)
        .all()
    )

    forum_stats = {
        "users": db.session.query(User).count(),
        "posts": db.session.query(ForumPost).count(),
        "comments": db.session.query(Comment).count()
    }

    poll = db.session.execute(db.select(Poll).where(Poll.id == CURRENT_POLL_ID)).scalars().first()
    options = db.session.execute(db.select(PollOption).where(PollOption.poll_id == CURRENT_POLL_ID)).scalars().all()

    user_has_voted = None
    if current_user.is_authenticated:
        user_has_voted = (
                db.session.query(PollVote).filter_by(user_id=current_user.id, poll_id=poll.id).first() is not None)

    return render_template(
        "index.html",
        all_posts=posts,
        categories=categories,
        selected_category=category_name,
        votes_by_post=votes_by_post,
        trending_posts=trending_posts,
        forum_stats=forum_stats,
        poll=poll,
        options=options,
        user_has_voted=user_has_voted
    )


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def view_post(post_id):
    requested_post = db.get_or_404(ForumPost, post_id)
    if request.method == "POST":
        posted_comment = request.form.get('comment')
        if posted_comment:
            new_comment = Comment(
                comment_author=current_user,
                parent_post=requested_post,
                text=posted_comment
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('view_post', post_id=post_id, current_user=current_user))

    comment_ids = [comment.id for comment in requested_post.comments]
    # Query all votes by the current user on all comments
    if current_user.is_authenticated:
        user_votes = {v.comment_id: v.value for v in CommentVote.query.filter(
            CommentVote.comment_id.in_(comment_ids),
            CommentVote.user_id == current_user.id
        ).all()}
    else:
        user_votes = {}
    return render_template("post.html", post=requested_post, current_user=current_user, user_votes=user_votes)


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


@app.route('/profile/<profile_username>')
def profile(profile_username):
    tab = request.args.get("tab", "all")
    user = db.session.execute(db.select(User).where(User.username == profile_username)).scalar()
    if user:
        return render_template("profile.html", user=user, tab=tab)
    else:
        return redirect(url_for('home'))


@app.route("/create-post", methods=["GET", "POST"])
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        category_id = request.form.get('category')
        new_post = ForumPost(
            title=form.title.data,
            body=form.body.data,
            author=current_user,
            date=datetime.now(),
            category=db.session.get(ForumCategories, int(category_id))
        )

        # Add the new post to the Database
        db.session.add(new_post)
        db.session.commit()

        # Index the new post in Elasticsearch
        index_post(new_post)

        return redirect(url_for('view_post', post_id=new_post.id))
    return render_template('create-post.html', form=form)


def handle_vote(model_class, vote_model, content_id_name, content_id_value, action):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    filters = {
        'user_id': current_user.id,
        content_id_name: content_id_value
    }

    existing_vote = vote_model.query.filter_by(**filters).first()
    value = 1 if action == "upvote" else -1

    if existing_vote:
        # Delete the existing vote if the same vote was cast
        if existing_vote.value == value:
            db.session.delete(existing_vote)
        # Otherwise change the vote
        else:
            existing_vote.value = value
    else:
        new_vote = vote_model(user_id=current_user.id, **{content_id_name: content_id_value}, value=value)
        db.session.add(new_vote)

    db.session.commit()
    return redirect(request.referrer or url_for('home'))


@app.route('/vote/post/<int:post_id>/<action>', methods=["POST"])
def vote_post(post_id, action):
    return handle_vote(ForumPost, PostVote, 'post_id', post_id, action)


@app.route('/vote/comment/<int:comment_id>/<action>', methods=["POST"])
def vote_comment(comment_id, action):
    return handle_vote(Comment, CommentVote, 'comment_id', comment_id, action)


@app.route("/vote_poll/<int:poll_id>", methods=["POST"])
def vote_poll(poll_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    option_id = request.form.get("option_id")

    # Prevent duplicate votes
    existing_vote = PollVote.query.filter_by(user_id=current_user.id, poll_id=poll_id).first()
    if existing_vote:
        return redirect(url_for("home"))

    vote = PollVote(user_id=current_user.id, poll_id=poll_id, option_id=option_id)
    db.session.add(vote)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)