import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Integer, nullable=False)

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def toMap(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role
        }


class News(Base):
    __tablename__ = 'News'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('User.id'))
    date = Column(DateTime, default=datetime.datetime.utcnow)

    author = relationship('User', backref='news')
    images = relationship('NewsImage')

    def __init__(self, title, description, author_id):
        self.title = title
        self.description = description
        self.author_id = author_id


class NewsImage(Base):
    __tablename__ = 'NewsImage'
    id = Column(Integer, primary_key=True, autoincrement=True)
    news_id = Column(Integer, ForeignKey('News.id'))
    url = Column(String(500))

    def __init__(self, news_id, url):
        self.news_id = news_id
        self.url = url
