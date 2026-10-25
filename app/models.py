from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class User(Base):

    __tablename__ = "users"

    # mapped_column is a function that creates a column. It takes options like primary_key=True, unique=True, nullable=False, index=True, or ForeignKey(...).
    # Mapped is a type annotation. It tells SQLAlchemy and type checkers the Python type of the

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True,nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_file: Mapped[str | None] = mapped_column(String(250), nullable=True, default=None,)

    posts: Mapped[list[Post]] = relationship(back_populates="author")

    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"

# This declares a one-to-many relationship: one user has many posts. It doesn’t create a column. It tells SQLAlchemy how to load the related rows as Python objects.

# Mapped[list[Post]] is the type annotation. It says user.posts is a list of Post objects. Like Mapped[int], it’s only a type hint.
# relationship(...) creates the link. It reads and writes rows in the posts table through a foreign key, so the Post model needs a ForeignKey pointing back at users.id.
# back_populates="author" keeps both sides in sync. It names the attribute on Post that points back to the user, so post.author and user.posts update each other in memory.

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    date_posted: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default= lambda: datetime.now(UTC)
    )


    author: Mapped[User] = relationship(back_populates="posts")