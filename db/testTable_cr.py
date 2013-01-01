import random 
import unittest
from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
import table_cr as db
import datetime as dt

def deco(func):
    print '.. > ', func
    return func

class TestDatabase:
    
    def getSession(self): 
        engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()  
        return session
    @deco
    def testAddUser(self):
        user = db.User(
            "superjom",
            "511541",
            "Shenzhen, Guangdong",
            "PKU",
            1,
            "./logo_url",
        )  
        session = self.getSession()
        session.add(user)
        session.commit()
    @deco
    def testAddTagKind(self):
        circlekind = db.TagKind("Sex")
        self.commit(circlekind)
    @deco
    def testAddTag(self):
        tag = db.Tag('Male')
        self.commit(tag)
    @deco
    def testTagKindAppendTag(self):
        print '..find tagkind'
        session = self.getSession()
        tagkind = session.query(db.TagKind).first()
        tag = session.query(db.Tag).first()
        tagkind.tagsappend(tag)
        session.add(tag)
        session.add(tagkind)
        print '..commit'
        session.commit()
    @deco
    def testAddCircleKind(self):
        circle = db.CircleKind("School institutes")
        self.commit(circle)
    @deco
    def testAddCircle(self):
        circle = db.Circle("circle1")
        self.commit(circle)
    @deco
    def testCircleKindAppendCircle(self):
        print '..find circlekind'
        session = self.getSession()
        circlekind = session.query(db.CircleKind).first()
        circle = session.query(db.Circle).first()
        circlekind.circles.append(circle)
        session.add(circle)
        session.add(circlekind)
        session.commit()
    @deco
    def testAddMessage(self):
        print 'create message'
        message = db.Message(
            "the title",
            "the summary",
            "the creator",
            0,
            dt.datetime.today()
        )
        print 'create messageitem'
        item = db.MessageItem(
            "the content"
        )
        session = self.getSession()
        message.item = item
        session.add_all([message, item])
        session.commit()
    @deco
    def testPushMessage(self):
        print 'search message'
        session = self.getSession()
        message = session.query(db.Message).first()
        print 'push'
        messagemeta = db.MessageMeta(message) 
        session.add_all([message, messagemeta])  
        print 'commit'
        session.commit()
    
    def commit(self, ob):
        session = self.getSession()
        session.add(ob)
        session.commit(ob)
    
if __name__ == '__main__':
    testbase = TestDatabase()
    testbase.testAddUser()
    testbase.testAddTagKind()
    t = testbase
    t.testAddTag()
    t.testAddCircleKind()
    t.testAddCircle()
    t.testCircleKindAppendCircle()
    t.testAddMessage()
    t.testPushMessage()
    
    