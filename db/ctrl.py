# -*- coding: utf-8 -*
'''
Created on 2012-12-19

@author: superjom
'''
import table_def as db
from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
import datetime


def transP(text):
    res = ''
    for l in text.split('\n'):
        l = '<p>' + l + '</p>'
        res += l
    return res

def userGetInfo(userid):
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(db.User).filter(db.User.id == userid).first()
    res = {
        'name': user.name,
        'pwd': user.pwd,
        #'logo_url': user.logo_url,
        'pos': user.pos,
        'university': user.university,
    }
    return res

# user_index  首页逻辑
def userInfo(userid):
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(db.User).filter(db.User.id == userid).first()
    res = {
        'name': user.name,
        'pwd': user.pwd,
        'email': user.email,
        #'logo_url': user.logo_url,
        'pos': user.pos,
        'university': user.university,
    }
    return res

def userGetMessages(userid):
    userid = 1
    
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(db.User).filter(db.User.id == userid).first()
    messages = user.messages
    count = len(messages)
    result = {}

    res = []
    result['messages'] = res
    result['count'] = count
    for m in messages:
        res.append(
            {
             'id':m.id,
             'title': m.title,
             'date': m.date,
             'summary': m.summary,
             'content': transP(m.item.content),
             }
        )
    return result

def userGetContent(contentid):
    '''
        传回内容״̬
    '''
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    message = session.query(db.Message).filter(db.Message.id == contentid).first()
    message.status = -1
    content = message.content
    return content


#-------------------------------- news -----------------------------------
import types
def getNews(station):
    '''
    get staton's all news
    station is id or string name

    title
    date
    '''
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    res = {}
    if type(station) is types.IntType:
        '''
        get id
        '''
        s = session.query(db.Station).filter(db.Station.id == station).first()
        news = s.news
        res['kind'] = s.name
    else:
        res['kind'] = station
        s = session.query(db.Station).filter(db.Station.name == station).first()
        news = s.news
    res['news'] = []
    for n in news:
        item = n.item
        res['news'].append(
            {
                'title':item.title,
                'station': item.station.name,
                'date':n.date,
            }
        )
    return res

def getAllNewsList():
    '''
    the news index
    '''
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()

    res = []
    news = session.query(db.News)
    for n in news:
        res.append({
            'id': n.id,
            'title': n.item.title,
            'date': n.date,
            'station': n.station.name
        })

def getNewsById(id):
    '''
    get news content:
    title
    date
    content
    station
    '''
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    news = session.query(db.News).filter(db.News.id == id).first()
    res = {}
    res['title'] = news.item.title
    res['content'] = news.item.content
    res['date'] = news.item.date
    res['station'] = news.station.name
    return res

def getStations():
    '''
    get stations:
    id
    name
    '''
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    stations = session.query(db.Station)
    res = []
    for s in stations:
        res.append(
            {'name': s.name,
            'id':s.id,
            }
        )
    return res

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class User:
    def __init__(self):
        self.user = None
        engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
        # create a Session
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def login(self, name, pwd):
        user = self.session.query(db.User.id, db.User.pwd)\
            .filter(db.User.name == name).first()
        if user:
            print 'succeed find user'
            print 'user:',user
            if user.pwd == pwd:
                return user.id
        return -1

    def getInfo(self, id):
        assert id != None, "No User here"
        #info = session.query(db.User.name, db.User.email, \
        #   db.User.university, db.User.pos).filter(db.User.id == self.userid).first()
        info = self.session.query(db.User.name, db.User.pos, db.User.university, db.User.email)\
                    .filter(db.User.id == id).first()
        #self.user.name, self.user.pos, self.user.university, self.user.email)
        return info 
    
    def getMessages(self):
        user = self.session.query(db.User).filter(db.User.id == self.userid).first()
        return user.messages()

    def getStations(self):
        return self.user.stations
    
    def getCircles(self):
        return self.user.circles
    
    
    def addNew(self, name, pwd, email, pos, university):
        user = db.User(name, pwd, email, pos, university)
        self.session.add(user)
        self.session.commit()
        print 'succeed add new user!'

class Message:
    def __init__(self):
        engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
        # create a Session
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
    def push(self, circle_id, title, summary, content):
        date = datetime.datetime.today()
        message = db.Message(title, 0, date)
        messageitem = db.MessageItem(content)
        #add relation
        message.item = messageitem
        circle = self.session.query(db.Circle).filter(db.Circle.id ==id).first()
        if circle:
            print "find circle OK!"
        users = circle.users
        for user in users:
            user.messages.append(message)
        
class Tag:
    def parseCmd(self, cmd):
        pass
    
class Circle:
    def __init__(self):
        engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
        # create a Session
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
    def addNew(self, name, logo_url, des):
        circle = db.Circle(name, logo_url, des)
        self.session.add(circle)
        self.session.commit()
        print "succed add session"
        
if __name__ == '__main__':
    '''
    ctrl = User()
    ctrl.addNew("superjom", "511541", "superjom@gmail.com", "Shenzhen", "Peking University")
    id = ctrl.login("superjom", "511541")
    print 'getid', id
    #info = ctrl.getInfo()
    #print info
    '''
    print getNews(1)

    
    
    
    
    
    
