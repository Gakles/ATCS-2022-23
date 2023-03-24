"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT, DATETIME
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    # Columns
    username = Column("username", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)

    following = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.follower_id",
                             secondaryjoin="User.username==Follower.following_id")
    
    followers = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.following_id",
                             secondaryjoin="User.username==Follower.follower_id",
                             overlaps="following")


class Follower(Base):
    __tablename__ = "followers"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    follower_id = Column('follower_id', TEXT, ForeignKey('users.username'))
    following_id = Column('following_id', TEXT, ForeignKey('users.username'))

class Tweet(Base):
    # TODO: Complete the class
    __tablename__ = "tweets"
    id = Column("id", INTEGER, primary_key=True)
    username_id = Column("username_id", ForeignKey("users.id"))
    tag_id = Column("tag_id", ForeignKey("tags.id"))
    date = Column("date", TEXT)
    time = Column("time", TEXT)
    date = Column("date", TEXT)
    time = Column("time", TEXT)
    username = relationship("User", back_populates="tweets")
    tweettag = relationship("TweetTag", back_populates="tags")
    pass

class Tag(Base):
    # TODO: Complete the class
    pass

class TweetTag(Base):
    # TODO: Complete the class
    pass
