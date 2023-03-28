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
    tweets = relationship("Tweet", back_populates="user")
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
    date = Column("date", TEXT)
    time = Column("time", TEXT)
    date = Column("date", TEXT)
    time = Column("time", TEXT)
    username = relationship("User", back_populates="tweets")
    tags = relationship("Tag", secondary="tweet_tags", back_populates="tweets")
    pass

class Tag(Base):
    # TODO: Complete the class
    __tablename__ = "tag"
    id = Column("id", INTEGER, primary_key=True)
    content = Column("content", TEXT)
    s = relationship("Tag", secondary="tweet_tags", back_populates="tweets")
    pass

class TweetTag(Base):
    # TODO: Complete the class
    __tablename__ = "tweettag"
    id = Column("id", INTEGER, primary_key=True)
    tweet_id = Column(INTEGER, ForeignKey('tweet.id'), primary_key=True)
    tag_id = Column(INTEGER, ForeignKey('tag.id'), primary_key=True)
    pass
