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
    def __init__(self):
        session = getSession()
        Ctrl.__init__(self, session, db.Message)
        
    def push(self, circleid, message_dic):
        self.session = getSession()
        circle = self.session.query(db.Circle).filter(db.Circle.id == circleid).first()

        users = circle.users
        for u in users:
            message = db.Message(
                message_dic['title'],
                message_dic['summary'],
                -1,
                dt.datetime.today(),
            )
            message.creator_id = message_dic['ownerid']
            item = db.MessageItem(message_dic['content'])
            message.item = item
            self.session.add(message)
            self.session.add(item)
            meta = db.MessageMeta(message, -1)
            print meta
            u.messages.append(meta)
            self.session.add_all([u, meta])
        self.session.commit()
        print '-------- messages -------'
    
    def addReply(self, messageid, reply):
        pass
    




if __name__ == '__main__':
    session = getSession()
    message = session.query(db.Message).first()
    m = Message()
    dic = {
        'title': 'the title',
        'summary':'the summary',
        'status' : -1,
        'date': dt.datetime.today(),
        'ownerid': 1,
        'content':'the content',
    }
    m.push(1, dic)

    print 'show user messages'
    user = session.query(db.User).filter(db.User.id == 1).first()
    metas = user.messages
    try:
        for m in metas:
            print m.message.title
    
    except:
        pass
        
