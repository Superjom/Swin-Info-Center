import datetime as dt
import sys
sys.path.append('../')
import db.table_cr as db
#import table_cr as db
from common import Ctrl, getSession

class CircleKind(Ctrl):
    def __init__(self):
        '''
        joint session
        '''
        session = getSession()
        self.session = getSession()
        Ctrl.__init__(self, session, db.CircleKind)

    def add(self, circle):
        self.session = getSession()
        self.commit(circle)

    def add_circle_byId(self, id, circle):
        #ck = self.session.query(db.CircleKind).filter(db.CircleKind.id == id).first()
        self.session = getSession()
        self.setCur(id)
        self.cur.circles.append(circle)
        self.commit_all([circle, self.cur])


class Circle(Ctrl):
    def __init__(self):
        '''
        joint session
        '''
        self.session = getSession()
        Ctrl.__init__(self, self.session, db.Circle)

    def add(self, circle):
        self.session = getSession()
        self.commit(circle)
    
    def add_user_byId(self, id, user):
        self.session = getSession()
        self.setCur(id)
        self.cur.users.append(user)
        self.commit_all([self.cur, user])

    def getUserNames(self, circleid):
        self.session = getSession()
        self.setCur(circleid)
        res = []
        for u in self.cur.users:
            res.append({
                        'name': u.name,
                        'logo_url':u.logo_url,
                        })
        return res

