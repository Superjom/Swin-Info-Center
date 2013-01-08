'''
Created on Jan 8, 2013

@author: chunwei
'''
import datetime as dt
import sys
sys.path.append('../../')
import db.table_cr as db
#import table_cr as db
from common import Ctrl, getSession

class Message(Ctrl):
    def __init__(self, session):
        Ctrl.__init__(self, session, db.Message)
        
    def push(self, circleid, message_dic):
        message = db.Message(
            message_dic['title'],
            message_dic['summary'],
            0,
            dt.datetime.today(),
        )
        item = db.MessageItem(message_dic['content'])
        message.item = item
        circle = self.session.query(db.Circle).filter(db.Circle.id == circleid).first()
        users = circle.users
        for u in users:
            meta = db.MessageMeta(message)
            u.messages.append(meta)
            self.session.add_all([u, meta])
        self.session.add(message)
        self.session.add(message.item)
        self.session.commit()
    
    def addReply(self, messageid, reply):
        pass
    




if __name__ == '__main__':
    session = getSession()
    message = session.query(db.Message).first()
    m = Message(session)
    m.push(1, message)
    print 'show user messages'
    user = session.query(db.User).filter(db.User.id == 1).first()
    metas = user.messages
    for m in metas:
        print m.message.title
    
        
