# coding: utf-8
from sqlalchemy import Column, Enum, ForeignKey, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from swagger_server.__main__ import db

Base = declarative_base()
metadata = Base.metadata


class Attatchment(db.Model):
    __tablename__ = 'attatchment'

    attatchment_id = Column(INTEGER(), primary_key=True)
    file_name = Column(String(32), nullable=False)
    message_id = Column(ForeignKey('message.message_id'), nullable=False, index=True)
    file_size = Column(INTEGER(), nullable=False)
    file_url = Column(String(255), nullable=False)

    message = relationship('Message')
