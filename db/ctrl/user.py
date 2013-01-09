# -*- coding: utf-8 -*
import datetime as dt
import sys
sys.path.append('../../')
import db.table_cr as db
#import table_cr as db
from common import Ctrl, getSession

def transP(text):
    res = ''
    if text:
        for l in text.split('\n'):
            l = '<p>' + l + '</p>'
            res += l
    return res


class User(Ctrl):
    def __init__(self):
        '''
        joint session
        '''
        session = getSession()
        Ctrl.__init__(self, session, db.User)

    def addTag(self, id, tag):
        #user = self.session.query(db.User).filter(db.User.id == id).first()
        self.session = getSession()
        self.setCur(id)
        self.cur.tags.append(tag)
        self.commit_all([self.cur, tag])

    def addCircle(self, id, circle):
        self.session = getSession()
        self.setCur(id)
        self.cur.circles.append(circle)
        self.commit_all(self.cur, circle)

    def login(self, name, pwd):
        self.session = getSession()
        session = getSession()
        user = self.get_byName(session, name)
        if user:
            print '>> login get user: ', user.name, user.pwd
            if user.pwd == pwd:
                return user.id
        return -1

    def getInfo(self, id):
        #user = self.get(id)
        session = getSession()
        user = session.query(db.User).filter(db.User.id == id).first()
        res = {
            'name': user.name,
            'pwd': user.pwd,
            #'logo_url': user.logo_url,
            'email': user.email,
            'pos': user.pos,
            'logo_url': user.logo_url,
            'university': user.university,
        }
        return res

    def getStations(self, id):
        '''
        取得其收录的新闻站点
        '''
        self.session = getSession()
        user = self.get(id)
        return user.stations
        
    
    def getMessages(self, id):
        '''
        取得 id 的 user 的所有message
        '''
        self.session = getSession()
        user = self.get(id)
        messages = user.messages
        res = []
        for m in messages:
            message = m.message
            try:
                res.append(
                    {
                     'id':message.id,
                     'title': message.title,
                     'date': message.date,
                     'summary': message.summary,
                     'content': transP(message.item.content),
                     }
                )
            except:
                print 'no message!'
        res.reverse()
        return res

    def getReplys(self, id):
        self.session = getSession()
        res = []
        user = self.get(id)
        replys = user.replys
        for r in replys:
            owner_id = r.owner_id
            #get from user
            from_user = self.get(owner_id)
            print r.replyto
            item = r.item
            try:
                res.append({
                    'id':r.id,
                    'replyto':r.replyto,
                    'date':r.date,
                    'content':item.content,
                    'from_user_name': from_user.name,
                    'from_user_logo_url': from_user.logo_url,
                })
            except:
                print 'none reply'
        return res

    def getAllNewsList(self, id, page=-1):
        self.session = getSession()
        news_page_num = 7
        res = []
        user = self.get(id)
        #split page
        if page == -1:
            news = user.news
        else:
            print user.news
            news = user.news[page * news_page_num : (page+1) * news_page_num]
        for n in news:
            res.append({
                'id': n.id,
                'title': n.title,
                'date': n.date,
                'station': n.station.name
            })
        return res
    
    def getCircles(self, id):
        self.session = getSession()
        user = self.get(id)
        circles = user.circles
        res = []
        for c in circles:
            res.append(
                {'id': c.id,
                'name': c.name,
                }
            )
        return res   
    
    def getTags(self, id):  
        self.session = getSession()  
        user = self.get(id)
        tags = user.tags
        res = []
        for t in tags:
            res.append(
                {'id': t.id,
                'name': t.name,
                }
            )
        return res        

if __name__ == '__main__':
    session = getSession()
    u = User(session)
    user = db.User(
        "chunwei" ,
        "511541",
        "superjom@gmail.com",
        "pos",
        "pku",
        1.0,
        "./"
    )
    #u.add(user)
    u.show_all()
    us =  u.get(1)
    circles = us.circles
    print 'circles'
    for c in circles:
        print c.name, c.id


