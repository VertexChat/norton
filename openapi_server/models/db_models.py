# coding: utf-8
from sqlalchemy import Column, Enum, ForeignKey, Index, Integer, String, TIMESTAMP, Table, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from openapi_server.__main__ import db

metadata = db.Model.metadata


class User(db.Model):
    __tablename__ = 'user'

    id = Column(INTEGER, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    password = Column(String(255), nullable=False)


class Channel(db.Model):
    __tablename__ = 'channel'
    __table_args__ = (
        Index('name', 'name', 'creator_id', 'type', unique=True),
    )

    id = Column(INTEGER, primary_key=True)
    name = Column(String(32), nullable=False)
    creator_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    type = Column(Enum('TEXT', 'VOICE'), nullable=False)

    creator = relationship('User')
    user = relationship('User', secondary='member')


class Session(db.Model):
    __tablename__ = 'session'

    id = Column(String(255), primary_key=True)
    user = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    expire_after = Column(Integer, nullable=False)

    user1 = relationship('User')


t_member = Table(
    'member', metadata,
    Column('channel', ForeignKey('channel.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    Column('user', ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Index('channel', 'channel', 'user', unique=True)
)


class Message(db.Model):
    __tablename__ = 'message'

    id = Column(INTEGER, primary_key=True)
    channel = Column(ForeignKey('channel.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    author = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    content = Column(String(255), nullable=False)
    timestamp = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship('User')
    channel1 = relationship('Channel')
