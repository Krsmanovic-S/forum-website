from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime
from datetime import datetime


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)

    posts = relationship("ForumPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")

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

    def __init__(self, title, body, date, author, category):
        self.title = title
        self.body = body
        self.date = date
        self.author = author
        self.category = category


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("forum_posts.id"))
    parent_comment_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("comments.id"), nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    comment_author = relationship("User", back_populates="comments")
    parent_post = relationship("ForumPost", back_populates="comments")
    parent_comment = relationship("Comment", remote_side=[id], backref=db.backref("replies", cascade="all, delete-orphan"))

    def __init__(self, comment_author, parent_post, text, parent_comment=None):
        self.comment_author = comment_author
        self.parent_post = parent_post
        self.text = text
        self.parent_comment = parent_comment
