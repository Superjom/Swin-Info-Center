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
    User Tag:       many to many
    User Circle:    many to many
    Station News:   one to many

    User Message:   one to many
    User Station:   many to many
    
    Message Item:   one to one
    News Item:      one to one
    Reply Item:     one to one
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

    # user.messages : one to many
    messages = relationship("Message")
    #many to many: user to station
    stations = relationship("Station",
            secondary = user_station_association,
            backref = "users"
    )

    def __init__(self, name, pwd, email, pos, university, score=1):
        self.name = name
        self.pwd = pwd
        self.email = email
        self.pos = pos
        self.university = university
        self.score = score

class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column(String(15))
    kind = Column(String(20))

    def __init__(self, name, kind):
        self.name = name
        self.kind = kind

class Circle(Base):
    __tablename__ = "circle"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    logo_url = Column(String)
    des = Column(String)
    kind = Column(String(10))

    def __init__(self, name, logo_url, des, kind):
        self.name = name
        self.logo_url = logo_url
        self.des = des
        self.kind = kind
    

#--------- items -------------------------
class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    #1 read, 0 unread, -1 saved
    status = Column(Integer)
    date = Column(Date)
    summary = Column(String)
    #user.messages:     user to message: one to many
    user_id = Column(Integer, ForeignKey("user.id"))
    #message.item   one to one
    item = relationship("MessageItem", uselist=False)

    def __init__(self, title, summary, status, date):
        self.title = title
        self.summary = summary
        self.status = status
        self.date = date

class Reply(Base):
    __tablename__ = "reply"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    status = Column(Integer)
    #reply.item     one to one
    item = relationship("ReplyItem", uselist=False)

    def __init__(self, date, status):
        self.date = date
        self.status = status


# --------- News -----------------------
class Station(Base):
    __tablename__ = "station"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    #Station to News: one to many
    news = relationship("News")
    
    def __init__(self, name):
        self.name = name

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    
    #Station  to News
    station_id = Column(Integer, ForeignKey("station.id"))
    station = Column(String(15))
    #news.item  news to Item: one to one
    item = relationship("NewsItem", uselist=False)

    def __init__(self, date):
        self.date = date

class MessageItem(Base):
    __tablename__ = 'messageitem'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    message_id = Column(Integer, ForeignKey('message.id'))

    def __init__(self, content):
        self.content = content

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

class ReplyItem(Base):
    __tablename__ = 'replyitem'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    reply_id = Column(Integer, ForeignKey('reply.id'))

    def __init__(self, content):
        self.content = content
        
# create tables
if __name__ == '__main__' :
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    Base.metadata.create_all(engine)
    print 'db ok!'
