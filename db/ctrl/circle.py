import datetime as dt
import sys
sys.path.append('../')
import db.table_cr as db
#import table_cr as db
from common import Ctrl

class CircleKind(Ctrl):
    def __init__(self, session):
        '''
        joint session
        '''
        Ctrl.__init__(session, db.CircleKind)

    def add(self, circle):
        self.commit(circle)

    def add_circle_byId(self, id, circle):
        #ck = self.session.query(db.CircleKind).filter(db.CircleKind.id == id).first()
        self.setCur(id)
        self.cur.circles.append(circle)
        self.commit_all([circle, self.cur])


class Circle(Ctrl):
    def __init__(self, session):
        '''
        joint session
        '''
        Ctrl.__init__(session, db.Circle)

    def add(self, circle):
        self.commit(circle)
    
    def add_user_byId(self, id, user):
        self.setCur(id)
        self.cur.users.append(user)
        self.commit_all([self.cur, user])

