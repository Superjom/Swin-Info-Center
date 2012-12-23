# -*- coding: utf-8 -*
'''
Created on 2012-12-19

@author: superjom
'''
import table_def as db
from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
import datetime

news_page_num = 7
message_page_num = 7

def createSession():
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

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

def userGetUpdateMessages(userid):
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    '''
    user = session.query(db.User).filter(db.User.id == userid).first()
    messages = user.messages
    res = []
    '''
    messages = session.query(db.Message).filter(db.Message.status == -1)
    res = []
    for m in messages:
        #change status to avoid duplicate change
        m.status = 0
        session.add(m)
        res.append(
            {
             'id':m.id,
             'title': m.title,
             'date': m.date,
             'summary': m.summary,
             'content': transP(m.item.content),
             }
        )
    session.commit()
    res.reverse()
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
    res.reverse()
    return result


def pushMessage(circle, filter_sql, title, summary, content, date = datetime.datetime.today()):
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=True)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    #find users by circle
    circle = session.query(db.Circle).filter(db.Circle.id == int(circle)).first()
    users = circle.users
    #filter users
    tem = []
    keywords = [word.strip() for word in filter_sql.split('AND')]
    for user in users:
        tags = [tag.name for tag in user.tags]
        flag = True
        for word in keywords:
            if not word: continue
            flag = flag and (word in tags)
        if flag:
            tem.append(user)
    users = tem 
    status = -1
    message = db.Message(title, summary, status, date)
    messageitem = db.MessageItem(content)
    message.item = messageitem
    session.add(message)
    session.add(messageitem)
    for user in users:
        print 'push to users:', user.name
        user.messages.append(message)
        session.add(user)
    session.commit()
        


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

#-------------------------------- tags ----------------
# filter users by tags and circle
def filterUsers(circle_id, tagsql):
    print '-'*50
    print 'filter:'
    print circle_id, tagsql
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    #find users by circle
    circle = session.query(db.Circle).filter(db.Circle.id == circle_id).first()
    users = circle.users
    print 'users', len(users)
    print len(users)
    #filter users
    tem = []
    keywords = [word.strip() for word in tagsql.split('AND')]
    for user in users:
        tags = [tag.name for tag in user.tags]
        #print 'tags:', tags
        #print 'keyword', keywords
        flag = True
        #print 'in?', keywords[0] in keywords
        for word in keywords:
            if not word: continue
            flag = flag and (word in tags)
        if flag:
            tem.append(user)
    print 'tem', tem
    #pack res
    res = []
    for user in tem:
        res.append({
            'id': user.id,
            'name': user.name,
            'logo_url':'',#user.logo_url,
        })
    print 'res', res
    return res
            

#-------------------------------- circle ---------------
def getAllCircleList():
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    circles = session.query(db.Circle)
    res = []
    for c in circles:
        res.append(
            {'id': c.id,
            'name': c.name,
            }
        )
    return res

def getUserCircle(user_id):
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    res = []
    user = session.query(db.User).filter(db.User.id == user_id).first()
    circles = user.circles
    for c in circles:
        res.append(
            {'id': c.id,
            'name': c.name,
            }
        )
    return res

#-------------------------------tags-------------------
def getUserTags(user_id):
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    res = []
    user = session.query(db.User).filter(db.User.id == user_id).first()
    tags = user.tags
    for t in tags:
        res.append(
            {'id': t.id,
            'name': t.name,
            }
        )
    return res

def getTags():
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    res = []
    tags = session.query(db.Tag)
    for t in tags:
        res.append(
            {'id': t.id,
            'name': t.name,
            }
        )
    return res
    
    
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
        res['station'] = s.name
    else:
        res['station'] = station
        s = session.query(db.Station).filter(db.Station.name == station).first()
        news = s.news
    res['news'] = []
    for n in news:
        item = n.item
        res['news'].append(
            {
                'id': n.id,
                'title':item.title,
                'station': n.station.name,
                'date':n.date,
            }
        )
    return res

def getAllNewsList(page=-1):
    '''
    the news index
    '''
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    res = []
    #split page
    if page == -1:
        news = session.query(db.News)
    else:
        news = session.query(db.News)[page * news_page_num : (page+1) * news_page_num]
    for n in news:
        res.append({
            'id': n.id,
            'title': n.item.title,
            'date': n.date,
            'station': n.station.name
        })
    return res

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
    res['date'] = news.date
    res['station'] = news.station.name
    return res

def getStationName(id):
    engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    name = session.query(db.Station.name).filter(db.Station.id == id).first()
    return name

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
            'num':len(s.news),
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
    print getAllNewsList()
    print filterUsers(1, u'橄榄球')
    '''
    messages =  userGetMessages(1)
    for m in messages['messages']:
        print m['title']

    
    
    

    
    
    
