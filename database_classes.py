from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Integer, String, Text, ForeignKey


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

    posts = relationship("ForumPost", back_populates="category")


class ForumPost(db.Model):
    __tablename__ = "forum_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("forum_categories.id"), nullable=False)

    author = relationship("User", back_populates="posts")
    category = relationship("ForumCategories", back_populates="posts")
    comments = relationship("Comment", back_populates="parent_post")


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    post_id: Mapped[str] = mapped_column(Integer, db.ForeignKey("forum_posts.id"))
    text: Mapped[str] = mapped_column(Text, nullable=False)

    comment_author = relationship("User", back_populates="comments")
    parent_post = relationship("ForumPost", back_populates="comments")

    parent_comment_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("comments.id"), nullable=True)
    replies = relationship("Comment", backref=db.backref('parent_comment', remote_side='Comment.id'))

    def __init__(self, comment_author, parent_post, text):
        self.comment_author = comment_author
        self.parent_post = parent_post
        self.text = text
