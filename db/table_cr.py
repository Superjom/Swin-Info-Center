# -*- coding: utf-8 -*
'''
Created on 2012-12-19

@author: superjom
'''
from sqlalchemy import Table, create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
'''
Relations:
    User Tag:               many to many
    User Circle:            many to many

    TagKind Tag:            one to many
    CircleKind Circle:      One to many

    User MessageMeta:       one to many
    MessagMeta message:     many to one
    Message MessageItem:    one to one


    User Station:           many to many
    Station News:           one to many
    
    Message Item:           one to one
    News Item:              one to one
    Reply Item:             one to one
'''
Base = declarative_base()

# relationship of user tag

user_tag_association = Table('user_tag_association', Base.metadata,
        Column("user_id", Integer, ForeignKey("user.id")),
        Column("tag_id", Integer, ForeignKey("tag.id")),
)

user_circle_association = Table('user_circle_association', Base.metadata,
        Column("user_id", Integer, ForeignKey("user.id")),
        Column("circle_id", Integer, ForeignKey("circle.id")),
)

admin_circle_association = Table('admin_circle_association', Base.metadata,
        Column("user_id", Integer, ForeignKey("user.id")),
        Column("circle_id", Integer, ForeignKey("circle.id")),
)

own_message_association = Table('own_message_association', Base.metadata,
        Column("user_id", Integer, ForeignKey("user.id")),
        Column("message_id", Integer, ForeignKey("message.id")),
)

# many user to many stations
user_station_association = Table('user_station_association', Base.metadata,
        Column("user_id", Integer, ForeignKey("user.id")),
        Column("station_id", Integer, ForeignKey("station.id")),
)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(10))
    pwd = Column(String(15))
    email = Column(String(25))
    pos = Column(String(25))
    university = Column(String(25))
    score = Column(Float)
    logo_url = Column(String)

    # more to more:  user to tag
    tags = relationship("Tag",
            secondary = user_tag_association,
            backref = "users"
    )
    #many to many: user to circle
    circles = relationship("Circle",
            secondary = user_circle_association,
            backref = "users"
    )
    #many to many: admin to circle
    owncircles = relationship("Circle",
            secondary = admin_circle_association,
            backref = "admins"
    )
    # admin to messages 
    # if one create a message, then he is the owner of 
    # this message
    ownmessages = relationship("Message",
            secondary = own_message_association,
            backref = "owners"
    )
    
    # user.messages : one to many meta
    # first get message status and then determine whether
    # to display the message
    # user has many messagemetas
    messages = relationship("MessageMeta")
    #many to many: user to station
    stations = relationship("Station",
            secondary = user_station_association,
            backref = "users"
    )
    # one to many: replys
    replys = relationship("Reply")

    def __init__(self, name, pwd, email, pos, university, score=1, logo_url=''):
        self.name = name
        self.pwd = pwd
        self.email = email
        self.pos = pos
        self.university = university
        self.score = score
        self.logo_url = logo_url

# ----------------- tags -------------------
class TagKind(Base):
    __tablename__ = "tagkind"
    id = Column(Integer, primary_key=True)
    name = Column(String(15))
    tags = relationship("Tag", backref="tagkind")
    def __init__(self, name):
        self.name = name

class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column(String(15))
    tagkind_id = Column(Integer, ForeignKey("tagkind.id"))

    def __init__(self, name):
        self.name = name

# ----------------- circles ---------------
class CircleKind(Base):
    __tablename__ = "circlekind"
    id = Column(Integer, primary_key=True)
    name = Column(String(15))
    circles = relationship("Circle", backref="circlekind")
    def __init__(self,name):
        self.name = name

class Circle(Base):
    __tablename__ = "circle"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    logo_url = Column(String)
    des = Column(String)
    circlekind_id = Column(Integer, ForeignKey("circlekind.id"))

    def __init__(self, name, logo_url, des):
        self.name = name
        self.logo_url = logo_url
        self.des = des

#--------- message -------------------------
class MessageMeta(Base):
    '''
    meta status information for each data
    '''
    __tablename__ = "messagemeta"
    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    #user.messages:     user to message: one to many
    user_id = Column(Integer, ForeignKey("user.id"))
    # one to one
    message = relationship("Message", uselist=False)
    def __init__(self, message, status=0):
        self.status = status
        self.message = message

class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    #1 read, 0 unread, -1 saved
    status = Column(Integer)
    date = Column(Date)
    summary = Column(String)
    # who create it
    creator = Column(String)
    #messagemeta
    messagemeta_id = Column(Integer, ForeignKey("messagemeta.id"))
    #message.item   one to one
    item = relationship("MessageItem", uselist=False)
    #follower
    followers = relationship("Follower")

    def __init__(self, title, summary, creator, status, date):
        self.title = title
        self.summary = summary
        self.status = status
        self.creator = creator
        self.date = date
        
class MessageItem(Base):
    __tablename__ = 'messageitem'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    message_id = Column(Integer, ForeignKey('message.id'))

    def __init__(self, content):
        self.content = content

# ------------ news ----------------------------
class Follower(Base):
    __tablename__ = "follower"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(Date)
    message_id = Column(Integer, ForeignKey("message.id"))
    #logo_url = Column(String)
    
    def __init__(self, name, date, logo_url=''):
        self.name = name
        self.date = date
        #self.logo_url = logo_url

class Reply(Base):
    __tablename__ = "reply"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    status = Column(Integer)
    #replyto
    replyto = Column(String)
    #reply.item     one to one
    item = relationship("ReplyItem", uselist=False)
    #many to one user
    user_id = Column(Integer, ForeignKey('user.id'))

    
    def __init__(self, date, status, replyto):
        self.date = date
        self.status = status
        self.replyto = replyto

class ReplyItem(Base):
    __tablename__ = 'replyitem'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    reply_id = Column(Integer, ForeignKey('reply.id'))

    def __init__(self, content):
        self.content = content
        

# --------- News -----------------------
class Station(Base):
    __tablename__ = "station"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    #Station to News: one to many
    news = relationship("News", backref="station")
    
    def __init__(self, name):
        self.name = name

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    
    #Station  to News
    station_id = Column(Integer, ForeignKey("station.id"))
    #news.item  news to Item: one to one
    item = relationship("NewsItem", uselist=False)

    def __init__(self, date):
        self.date = date

class NewsItem(Base):
    __tablename__ = 'newsitem'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    #summary = Column(String)
    content = Column(String)
    news_id = Column(Integer, ForeignKey('news.id'))

    def __init__(self, title, content):
        self.title = title
        self.content = content

# create tables
if __name__ == '__main__' :
    engine = create_engine('sqlite:////home/chunwei/swin2/db/database.db', echo=True)
    Base.metadata.create_all(engine)
    print 'db ok!'
