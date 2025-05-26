from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, Enum
from datetime import datetime
import enum


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class GenderEnum(enum.Enum):
    NOT_SPECIFIED = "Not specified"
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(500), default="", nullable=True)
    date_of_birth: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    years_training: Mapped[int] = mapped_column(Integer, default=0)
    gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum), default=GenderEnum.NOT_SPECIFIED, nullable=False)

    posts = relationship("ForumPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")
    post_votes = db.relationship('PostVote', back_populates='user', cascade="all, delete-orphan")
    comment_votes = db.relationship('CommentVote', back_populates='user', cascade="all, delete-orphan")
    poll_votes = db.relationship('PollVote', back_populates='user', cascade="all, delete-orphan")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class ForumCategories(db.Model):
    __tablename__ = "forum_categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    posts = relationship("ForumPost", back_populates="category")


class ForumPost(db.Model):
    __tablename__ = "forum_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("forum_categories.id"), nullable=False)

    author = relationship("User", back_populates="posts")
    category = relationship("ForumCategories", back_populates="posts")
    comments = relationship("Comment", back_populates="parent_post", cascade="all, delete-orphan")
    votes = db.relationship('PostVote', back_populates='post', cascade="all, delete-orphan")

    def __init__(self, title, body, date, author, category):
        self.title = title
        self.body = body
        self.date = date
        self.author = author
        self.category = category


    @property
    def score(self):
        return sum(v.value for v in self.votes)


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("forum_posts.id"))
    parent_comment_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("comments.id"), nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    

    comment_author = relationship("User", back_populates="comments")
    parent_post = relationship("ForumPost", back_populates="comments")
    parent_comment = relationship("Comment", remote_side=[id], backref=db.backref("replies", cascade="all, delete-orphan"))
    votes = db.relationship('CommentVote', back_populates='comment', cascade="all, delete-orphan")

    def __init__(self, comment_author, parent_post, text, parent_comment=None):
        self.comment_author = comment_author
        self.parent_post = parent_post
        self.text = text
        self.parent_comment = parent_comment


    @property
    def score(self):
        return sum(v.value for v in self.votes)


class PostVote(db.Model):
    __tablename__ = 'post_votes'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id'), nullable=False)

    user = db.relationship('User', back_populates='post_votes')
    post = db.relationship('ForumPost', back_populates='votes')


class CommentVote(db.Model):
    __tablename__ = 'comment_votes'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)  # +1 or -1

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)

    user = db.relationship('User', back_populates='comment_votes')
    comment = db.relationship('Comment', back_populates='votes')


class Poll(db.Model):
    __tablename__ = 'polls'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)

    options = db.relationship('PollOption', back_populates='poll', cascade='all, delete-orphan')
    votes = db.relationship('PollVote', back_populates='poll', cascade='all, delete-orphan')


class PollOption(db.Model):
    __tablename__ = 'poll_options'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=False)

    poll = db.relationship('Poll', back_populates='options')
    votes = db.relationship('PollVote', back_populates='option', cascade='all, delete-orphan')


class PollVote(db.Model):
    __tablename__ = 'poll_votes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('poll_options.id'), nullable=False)

    user = db.relationship('User')
    poll = db.relationship('Poll', back_populates='votes')
    option = db.relationship('PollOption', back_populates='votes')