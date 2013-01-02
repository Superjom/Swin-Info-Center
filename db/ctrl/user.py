# -*- coding: utf-8 -*
import datetime as dt
import sys
sys.path.append('../../')
import db.table_cr as db
#import table_cr as db
from common import Ctrl, getSession

def transP(text):
    res = ''
    for l in text.split('\n'):
        l = '<p>' + l + '</p>'
        res += l
    return res


class User(Ctrl):
    def __init__(self, session):
        '''
        joint session
        '''
        Ctrl.__init__(self, session, db.User)

    def addTag(self, id, tag):
        #user = self.session.query(db.User).filter(db.User.id == id).first()
        self.setCur(id)
        self.cur.tags.append(tag)
        self.commit_all([self.cur, tag])

    def addCircle(self, id, circle):
        self.setCur(id)
        self.cur.circles.append(circle)
        self.commit_all(self.cur, circle)

    def login(self, name, pwd):
        user = self.get_byName(name)
        if user:
            print '*' * 50
            print '>> login get user: ', user.name, user.pwd
            if user.pwd == pwd:
                return user.id
        return -1

    def getInfo(self, id):
        user = self.get(id)
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
        user = self.get(id)
        return user.stations
        
    
    def getMessages(self, id):
        '''
        取得 id 的 user 的所有message
        '''
        user = self.get(id)
        messages = user.messages
        res = []
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
        return res

    def getAllNewsList(self, id, page=-1):
        news_page_num = 7
        res = []
        user = self.get(id)
        #split page
        if page == -1:
            news = user.news
        else:
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
    u.add(user)
    u.show_all()
    print u.get(1)

